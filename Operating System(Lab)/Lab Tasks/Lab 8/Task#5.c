#include <stdio.h>
#include <pthread.h>

typedef struct {
    int *arr;
    int start;
    int end;
    int count;
} Data;

int isPrime(int n) {
    if(n < 2) return 0;

    for(int i=2;i*i<=n;i++)
        if(n%i==0) return 0;

    return 1;
}

void *primeCount(void *arg) {
    Data *d=(Data*)arg;

    d->count=0;

    for(int i=d->start;i<d->end;i++)
        if(isPrime(d->arr[i])) d->count++;

    return NULL;
}

int main() {
    int arr[]={2,3,4,5,6,7,11,12,13,17};
    int n=10,t=2;

    pthread_t th[t];
    Data data[t];

    int part=n/t;

    for(int i=0;i<t;i++) {
        data[i].arr=arr;
        data[i].start=i*part;
        data[i].end=(i==t-1)?n:(i+1)*part;
        pthread_create(&th[i],NULL,primeCount,&data[i]);
    }

    int total=0;

    for(int i=0;i<t;i++) {
        pthread_join(th[i],NULL);
        total+=data[i].count;
    }

    printf("Prime Numbers = %d\n",total);

    return 0;
}
