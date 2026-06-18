#include <stdio.h>
#include <pthread.h>

int marks[] = {60,75,90,45,88,55,70,95};
int n = 8;

double avg;
int highest, lowest, passed;

void *average(void *arg) {
    int sum = 0;
    for(int i=0;i<n;i++) sum += marks[i];
    avg = (double)sum/n;
    return NULL;
}

void *high(void *arg) {
    highest = marks[0];
    for(int i=1;i<n;i++)
        if(marks[i] > highest) highest = marks[i];
    return NULL;
}

void *low(void *arg) {
    lowest = marks[0];
    for(int i=1;i<n;i++)
        if(marks[i] < lowest) lowest = marks[i];
    return NULL;
}

void *pass(void *arg) {
    passed = 0;
    for(int i=0;i<n;i++)
        if(marks[i] >= 50) passed++;
    return NULL;
}

int main() {
    pthread_t t1,t2,t3,t4;

    pthread_create(&t1,NULL,average,NULL);
    pthread_create(&t2,NULL,high,NULL);
    pthread_create(&t3,NULL,low,NULL);
    pthread_create(&t4,NULL,pass,NULL);

    pthread_join(t1,NULL);
    pthread_join(t2,NULL);
    pthread_join(t3,NULL);
    pthread_join(t4,NULL);

    printf("Average = %.2f\n",avg);
    printf("Highest = %d\n",highest);
    printf("Lowest = %d\n",lowest);
    printf("Passed = %d\n",passed);

    return 0;
}
