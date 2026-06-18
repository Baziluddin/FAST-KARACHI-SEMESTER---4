#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

typedef struct {
    char *filename;
    long start;
    long end;
    int count;
} Data;

void *countLines(void *arg) {
    Data *d = (Data *)arg;
    FILE *fp = fopen(d->filename, "r");

    fseek(fp, d->start, SEEK_SET);

    if (d->start != 0) {
        int ch;
        while ((ch = fgetc(fp)) != '\n' && ftell(fp) < d->end);
    }

    int c;
    d->count = 0;

    while (ftell(fp) < d->end && (c = fgetc(fp)) != EOF) {
        if (c == '\n')
            d->count++;
    }

    fclose(fp);
    return NULL;
}

int main() {
    char filename[] = "log.txt";
    int n = 4;

    FILE *fp = fopen(filename, "r");
    fseek(fp, 0, SEEK_END);
    long size = ftell(fp);
    fclose(fp);

    pthread_t threads[n];
    Data data[n];

    long chunk = size / n;

    for (int i = 0; i < n; i++) {
        data[i].filename = filename;
        data[i].start = i * chunk;
        data[i].end = (i == n - 1) ? size : (i + 1) * chunk;
        pthread_create(&threads[i], NULL, countLines, &data[i]);
    }

    int total = 0;

    for (int i = 0; i < n; i++) {
        pthread_join(threads[i], NULL);
        total += data[i].count;
    }

    printf("Total Requests = %d\n", total);
    return 0;
}
