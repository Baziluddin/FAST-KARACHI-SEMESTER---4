#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

typedef struct {
    char *file;
    int words;
} Data;

void *countWords(void *arg) {
    Data *d=(Data*)arg;

    FILE *fp=fopen(d->file,"r");

    char word[100];
    d->words=0;

    while(fscanf(fp,"%s",word)==1)
        d->words++;

    fclose(fp);

    return NULL;
}

int main() {
    char *files[]={"a.txt","b.txt","c.txt"};
    int n=3;

    pthread_t th[n];
    Data data[n];

    for(int i=0;i<n;i++) {
        data[i].file=files[i];
        pthread_create(&th[i],NULL,countWords,&data[i]);
    }

    int total=0;

    for(int i=0;i<n;i++) {
        pthread_join(th[i],NULL);
        printf("%s = %d\n",files[i],data[i].words);
        total+=data[i].words;
    }

    printf("Total Words = %d\n",total);

    return 0;
}
