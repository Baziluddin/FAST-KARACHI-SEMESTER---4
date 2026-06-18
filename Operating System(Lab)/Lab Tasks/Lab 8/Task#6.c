#include <stdio.h>
#include <pthread.h>

int balance = 1000;

void *deposit(void *arg) {
    for(int i=0;i<10000;i++)
        balance += 10;
    return NULL;
}

void *withdraw(void *arg) {
    for(int i=0;i<10000;i++)
        balance -= 10;
    return NULL;
}

int main() {
    pthread_t t1,t2;

    pthread_create(&t1,NULL,deposit,NULL);
    pthread_create(&t2,NULL,withdraw,NULL);

    pthread_join(t1,NULL);
    pthread_join(t2,NULL);

    printf("Final Balance = %d\n",balance);

    return 0;
}
