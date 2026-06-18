#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

#define MAX_FLIGHTS 10
#define RUNWAYS 3
#define THRESHOLD 5

typedef enum { LANDING, EMERGENCY, TAKEOFF, CARGO } FlightType;

typedef struct {
    int id;
    FlightType type;
    int priority;
    time_t arrivalTime;
} Flight;

Flight pq[MAX_FLIGHTS];
int size = 0;

typedef struct {
    int busy;
    int blocked;
    int current_flight_id;
} Runway;

Runway runways[RUNWAYS];

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;

int flight_id = 0;
int stop = 0;
int generated = 0;

void swap(int i, int j)
{
    Flight t = pq[i];
    pq[i] = pq[j];
    pq[j] = t;
}

void heapify_up(int i)
{
    while (i > 0 && pq[i].priority > pq[(i - 1) / 2].priority)
    {
        swap(i, (i - 1) / 2);
        i = (i - 1) / 2;
    }
}

void heapify_down(int i)
{
    int largest = i;
    int l = 2*i + 1;
    int r = 2*i + 2;

    if (l < size)
    {
        if (pq[l].priority > pq[largest].priority)
        {
            largest = l;
        }
    }

    if (r < size)
    {
        if (pq[r].priority > pq[largest].priority)
        {
            largest = r;
        }
    }

    if (largest != i)
    {
        swap(i, largest);
        heapify_down(largest);
    }
}

void PushFlight(Flight f)
{
    if (size >= MAX_FLIGHTS)
    {
        return;
    }

    pq[size] = f;
    heapify_up(size);
    size++;
}

Flight PopFlight()
{
    Flight f = pq[0];
    pq[0] = pq[size - 1];
    size--;
    heapify_down(0);
    return f;
}

int ActualPriority(FlightType Type)
{
    if (Type == EMERGENCY)
    {
        return 10000;
    }

    if (Type == LANDING)
    {
        return 600;
    }

    if (Type == TAKEOFF)
    {
        return 300;
    }

    return 200;
}

void Update_Priorities()
{
    time_t now = time(NULL);
    printf("Updating The Priorities.");

    for (int s = 0; s < size; s++)
    {
        int wt = difftime(now, pq[s].arrivalTime);

        pq[s].priority = ActualPriority(pq[s].type);
        pq[s].priority += wt * 10;

        if (wt > THRESHOLD)
        {
            if (pq[s].type == LANDING)
            {
                pq[s].priority += 500;
            }

            if (pq[s].type == TAKEOFF)
            {
                pq[s].priority -= 200;
            }

            if (wt > 2 * THRESHOLD)
            {
                pq[s].priority += 300;
            }
        }
    }

    for (int i = size/2 - 1; i >= 0; i--)
    {
        heapify_down(i);
    }
}

int Emergency()
{
    for (int i = 0; i < size; i++)
    {
        if (pq[i].type == EMERGENCY)
        {
            return i;
        }
    }
    return -1;
}

Flight GetEmergency()
{
    int idx = Emergency();
    Flight f = pq[idx];

    pq[idx] = pq[size - 1];
    size--;

    heapify_down(idx);
    heapify_up(idx);

    return f;
}

void* FlightGenerator(void* arg)
{
    while (1)
    {
        sleep(rand()%3 + 1);

        pthread_mutex_lock(&lock);

        if (generated >= MAX_FLIGHTS)
        {
            stop = 1;
            pthread_cond_broadcast(&cond);
            pthread_mutex_unlock(&lock);
            break;
        }

        Flight f;

        f.id = flight_id;
        flight_id++;
        generated++;

        f.type = rand()%4;
        f.priority = ActualPriority(f.type);
        f.arrivalTime = time(NULL);

        PushFlight(f);

        printf("GeneraedFlight : %d and  Type: is  %d\n", f.id, f.type);

        pthread_cond_broadcast(&cond);
        pthread_mutex_unlock(&lock);
    }

    return NULL;
}

void* EmergencyMonitor(void* arg)
{
    while (stop == 0)
    {
        sleep(1);

        pthread_mutex_lock(&lock);

        int idx = Emergency();

        if (idx != -1)
        {
            pq[idx].priority = 20000;
            heapify_up(idx);

            printf("Emergency detected. Priority Boosted \n");
            pthread_cond_broadcast(&cond);
        }

        pthread_mutex_unlock(&lock);
    }

    return NULL;
}

void* RunwayController(void* arg)
{
    int id = *(int*)arg;

    while (stop == 0)
    {
        pthread_mutex_lock(&lock);

        while ((size == 0 || runways[id].blocked) && stop == 0)
        {
            pthread_cond_wait(&cond, &lock);
        }

        if (stop == 1 && size == 0)
        {
            pthread_mutex_unlock(&lock);
            break;
        }

        Update_Priorities();

        Flight f;
        int e_idx = Emergency();

        if (e_idx != -1)
        {
            f = GetEmergency();
        }
        else
        {
            f = PopFlight();
        }

        runways[id].busy = 1;
        runways[id].current_flight_id = f.id;

        pthread_mutex_unlock(&lock);

        printf("Runway : %d handling Flight : %d Type : %d \n", id, f.id, f.type);
        for (int i = 0; i < 4; i++)
        {
            sleep(1);
            pthread_mutex_lock(&lock);
            if (Emergency() != -1 && f.type != EMERGENCY)
            {
                printf("Runway %d PREEMPTED Flight %d\n", id, f.id);
                PushFlight(f);
                runways[id].busy = 0;
                runways[id].current_flight_id = -1;
                pthread_cond_broadcast(&cond);
                pthread_mutex_unlock(&lock);
                goto next_cycle;
            }

            pthread_mutex_unlock(&lock);
        }

        pthread_mutex_lock(&lock);
        printf("Runway %d finished Flight %d\n", id, f.id);
        runways[id].busy = 0;
        runways[id].current_flight_id = -1;
        pthread_mutex_unlock(&lock);
        next_cycle:;
    }

    return NULL;
}

void* Maintenance(void* arg)
{
    printf("Maintenance of the Runway Been done. ");

    while (stop == 0)
    {
        sleep(6);

        pthread_mutex_lock(&lock);

        int r = rand()%RUNWAYS;

        if (runways[r].busy == 0)
        {
            runways[r].blocked = 1;
            printf("Runway %d is now blocked for use .\n", r);
        }

        pthread_mutex_unlock(&lock);
        sleep(3);
        pthread_mutex_lock(&lock);
        runways[r].blocked = 0;
        printf("Runway %d is now available for use .\n", r);
        pthread_cond_broadcast(&cond);
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main()
{
    srand(time(NULL));
    pthread_t gen;
    pthread_t monitor;
    pthread_t maint;
    pthread_t rthreads[RUNWAYS];
    int ids[RUNWAYS];
    for (int i = 0; i < RUNWAYS; i++)
    {
        runways[i].busy = 0;
        runways[i].blocked = 0;
        runways[i].current_flight_id = -1;
        ids[i] = i;
    }

    pthread_create(&gen, NULL, FlightGenerator, NULL);
    pthread_create(&monitor, NULL, EmergencyMonitor, NULL);
    pthread_create(&maint, NULL, Maintenance, NULL);

    for (int i = 0; i < RUNWAYS; i++)
    {
        pthread_create(&rthreads[i], NULL, RunwayController, &ids[i]);
    }

    pthread_join(gen, NULL);
    pthread_join(monitor, NULL);
    pthread_join(maint, NULL);

    for (int i = 0; i < RUNWAYS; i++)
    {
        pthread_join(rthreads[i], NULL);
    }

    return 0;
}
