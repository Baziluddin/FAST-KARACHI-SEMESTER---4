#include <stdio.h>
#include <pthread.h>

typedef struct {
    int *votes;
    int size;
    int total;
} Region;

void *countVotes(void *arg) {
    Region *r=(Region*)arg;

    r->total=0;

    for(int i=0;i<r->size;i++)
        r->total+=r->votes[i];

    return NULL;
}

int main() {
    int r1[]={100,120,90};
    int r2[]={80,110,95};
    int r3[]={150,140,130};

    Region regions[3]={
        {r1,3,0},
        {r2,3,0},
        {r3,3,0}
    };

    pthread_t th[3];

    for(int i=0;i<3;i++)
        pthread_create(&th[i],NULL,countVotes,&regions[i]);

    int grandTotal=0;

    for(int i=0;i<3;i++) {
        pthread_join(th[i],NULL);
        grandTotal+=regions[i].total;
    }

    printf("Total Votes = %d\n",grandTotal);

    return 0;
}
