#include <stdio.h>
#include <pthread.h>

typedef struct {
    double *ratings;
    int start;
    int end;
    double sum;
} Data;

void *average(void *arg) {
    Data *d=(Data*)arg;

    d->sum=0;

    for(int i=d->start;i<d->end;i++)
        d->sum+=d->ratings[i];

    return NULL;
}

int main() {
    double ratings[]={4,5,3,4,5,2,5,4};
    int n=8,t=2;

    pthread_t th[t];
    Data data[t];

    int part=n/t;

    for(int i=0;i<t;i++) {
        data[i].ratings=ratings;
        data[i].start=i*part;
        data[i].end=(i==t-1)?n:(i+1)*part;
        pthread_create(&th[i],NULL,average,&data[i]);
    }

    double total=0;

    for(int i=0;i<t;i++) {
        pthread_join(th[i],NULL);
        total+=data[i].sum;
    }

    printf("Overall Average = %.2f\n",total/n);

    return 0;
}
