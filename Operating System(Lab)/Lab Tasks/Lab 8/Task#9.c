#include <stdio.h>
#include <pthread.h>

int results[3];

int factorial(int n) {
    int f=1;
    for(int i=1;i<=n;i++) f*=i;
    return f;
}

void *square(void *arg) {
    int n=*(int*)arg;
    results[0]=n*n;
    return NULL;
}

void *cube(void *arg) {
    int n=*(int*)arg;
    results[1]=n*n*n;
    return NULL;
}

void *fact(void *arg) {
    int n=*(int*)arg;
    results[2]=factorial(n);
    return NULL;
}

int main() {
    int n=5;

    pthread_t t1,t2,t3;

    pthread_create(&t1,NULL,square,&n);
    pthread_create(&t2,NULL,cube,&n);
    pthread_create(&t3,NULL,fact,&n);

    pthread_join(t1,NULL);
    pthread_join(t2,NULL);
    pthread_join(t3,NULL);

    printf("Square = %d\n",results[0]);
    printf("Cube = %d\n",results[1]);
    printf("Factorial = %d\n",results[2]);

    return 0;
}
