#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define BUFFER_SIZE 5

int buffer[BUFFER_SIZE];
int in = 0;
int out = 0;

pthread_mutex_t mutex;
sem_t empty;
sem_t full;

void *producer(void *arg)
{
    int id = *(int *)arg;

    for (int i = 1; i <= 5; i++)
    {
        int order = id * 100 + i;

        sem_wait(&empty);
        pthread_mutex_lock(&mutex);

        buffer[in] = order;
        printf("Producer %d produced Order %d at %d\n", id, order, in);

        in = (in + 1) % BUFFER_SIZE;

        pthread_mutex_unlock(&mutex);
        sem_post(&full);

        sleep(rand() % 2 + 1);
    }

    return NULL;
}

void *consumer(void *arg)
{
    int id = *(int *)arg;

    for (int i = 1; i <= 5; i++)
    {
        sem_wait(&full);
        pthread_mutex_lock(&mutex);

        int order = buffer[out];

        printf("Consumer %d processed Order %d from %d\n", id, order, out);

        out = (out + 1) % BUFFER_SIZE;

        pthread_mutex_unlock(&mutex);
        sem_post(&empty);

        sleep(rand() % 3 + 1);
    }

    return NULL;
}

int main()
{
    pthread_t producers[2], consumers[2];
    int p[2], c[2];

    pthread_mutex_init(&mutex, NULL);

    sem_init(&empty, 0, BUFFER_SIZE);
    sem_init(&full, 0, 0);

    for (int i = 0; i < 2; i++)
    {
        p[i] = i + 1;
        pthread_create(&producers[i], NULL, producer, &p[i]);
    }

    for (int i = 0; i < 2; i++)
    {
        c[i] = i + 1;
        pthread_create(&consumers[i], NULL, consumer, &c[i]);
    }

    for (int i = 0; i < 2; i++)
        pthread_join(producers[i], NULL);

    for (int i = 0; i < 2; i++)
        pthread_join(consumers[i], NULL);

    pthread_mutex_destroy(&mutex);

    sem_destroy(&empty);
    sem_destroy(&full);

    return 0;
}
