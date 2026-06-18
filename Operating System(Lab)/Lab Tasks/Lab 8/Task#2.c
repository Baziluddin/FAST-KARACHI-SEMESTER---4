#include <stdio.h>
#include <pthread.h>

typedef struct {
    double *orders;
    int start;
    int end;
    double subtotal;
} Data;

void *revenue(void *arg) {
    Data *d = (Data *)arg;

    d->subtotal = 0;

    for (int i = d->start; i < d->end; i++)
        d->subtotal += d->orders[i];

    return NULL;
}

int main() {
    double orders[] = {100,200,300,400,500,600,700,800};
    int n = 8;
    int t = 4;

    pthread_t th[t];
    Data data[t];

    int part = n / t;

    for (int i = 0; i < t; i++) {
        data[i].orders = orders;
        data[i].start = i * part;
        data[i].end = (i == t - 1) ? n : (i + 1) * part;
        pthread_create(&th[i], NULL, revenue, &data[i]);
    }

    double total = 0;

    for (int i = 0; i < t; i++) {
        pthread_join(th[i], NULL);
        total += data[i].subtotal;
    }

    printf("Total Revenue = %.2f\n", total);

    return 0;
}
