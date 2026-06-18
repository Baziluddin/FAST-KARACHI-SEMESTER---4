#include <stdio.h>
#include <string.h>
#include <pthread.h>

typedef struct {
    char *text;
    char *key;
    int start;
    int end;
    int count;
} Data;

void *search(void *arg) {
    Data *d = (Data *)arg;

    int len = strlen(d->key);
    d->count = 0;

    for(int i=d->start;i<=d->end-len;i++) {
        if(strncmp(&d->text[i], d->key, len) == 0)
            d->count++;
    }
    return NULL;
}

int main() {
    char text[]="hello world hello world hello";
    char key[]="hello";

    int n=2;
    pthread_t th[n];
    Data data[n];

    int len=strlen(text);
    int part=len/n;

    for(int i=0;i<n;i++) {
        data[i].text=text;
        data[i].key=key;
        data[i].start=i*part;
        data[i].end=(i==n-1)?len:(i+1)*part+strlen(key);
        pthread_create(&th[i],NULL,search,&data[i]);
    }

    int total=0;

    for(int i=0;i<n;i++) {
        pthread_join(th[i],NULL);
        total+=data[i].count;
    }

    printf("Occurrences = %d\n",total);

    return 0;
}
