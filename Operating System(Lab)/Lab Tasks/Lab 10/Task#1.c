#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

int readCount = 0;
int data = 0;

pthread_mutex_t mutex;
sem_t resource;
sem_t serviceQueue;

void *reader(void *arg)
{
    int id = *(int *)arg;

    sem_wait(&serviceQueue);

    pthread_mutex_lock(&mutex);
    readCount++;

    if (readCount == 1)
        sem_wait(&resource);

    pthread_mutex_unlock(&mutex);

    sem_post(&serviceQueue);

    printf("Reader %d reading data = %d\n", id, data);
    sleep(1);

    pthread_mutex_lock(&mutex);
    readCount--;

    if (readCount == 0)
        sem_post(&resource);

    pthread_mutex_unlock(&mutex);

    return NULL;
}

void *writer(void *arg)
{
    int id = *(int *)arg;

    sem_wait(&serviceQueue);
    sem_wait(&resource);
    sem_post(&serviceQueue);

    data++;

    printf("Writer %d updated data = %d\n", id, data);
    sleep(1);

    sem_post(&resource);

    return NULL;
}

int main()
{
    pthread_t readers[5], writers[2];
    int r[5], w[2];

    pthread_mutex_init(&mutex, NULL);
    sem_init(&resource, 0, 1);
    sem_init(&serviceQueue, 0, 1);

    for (int i = 0; i < 5; i++)
    {
        r[i] = i + 1;
        pthread_create(&readers[i], NULL, reader, &r[i]);
    }

    for (int i = 0; i < 2; i++)
    {
        w[i] = i + 1;
        pthread_create(&writers[i], NULL, writer, &w[i]);
    }

    for (int i = 0; i < 5; i++)
        pthread_join(readers[i], NULL);

    for (int i = 0; i < 2; i++)
        pthread_join(writers[i], NULL);

    pthread_mutex_destroy(&mutex);
    sem_destroy(&resource);
    sem_destroy(&serviceQueue);

    return 0;
}
