#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

int *arr;
int n;
double average;
int minimum;
int maximum;

void * calc_avg(void *arg)
{
    int sum = 0;
    for (int i = 0; i < n; i++)
    {
        sum += arr[i];
    }
    average = (double)sum / n;
    pthread_exit(0);
}

void * calc_min(void *arg)
{
    minimum = arr[0];
    for (int i = 1; i < n; i++)
    {
        if (arr[i] < minimum)
        {
            minimum = arr[i];
        }
    }
    pthread_exit(0);
}


void *calc_max(void *arg) 
{
    maximum = arr[0];
    for (int i = 1; i < n; i++)
    {
        if (arr[i] > maximum)
        {
            maximum = arr[i];
        }
    }
    pthread_exit(0);
}

int main(int argc, char *argv[])
{

    n = argc - 1;
    arr = (int *)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++)
    {
        arr[i] = atoi(argv[i + 1]);
    }

    pthread_t t1, t2, t3;
    pthread_create(&t1, NULL, calc_avg, NULL);
    pthread_create(&t2, NULL, calc_min, NULL);
    pthread_create(&t3, NULL, calc_max, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_join(t3, NULL);
    printf("The average value is %.0f\n", average);
    printf("The minimum value is %d\n", minimum);
    printf("The maximum value is %d\n", maximum);

    free(arr);
    return 0;
}
