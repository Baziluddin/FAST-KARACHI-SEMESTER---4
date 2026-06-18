#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

#define MAX 100
#define DOCTORS 4

typedef enum {CRITICAL, SERIOUS, NORMAL} PatientType;
typedef enum {SENIOR, JUNIOR} DoctorType;

typedef struct {
  int id;
  PatientType type;
  time_t arrival;
  } Patient;

Patient cq[MAX];
Patient sq[MAX];
Patient nq[MAX];

int cf=0;
int cr=0;
int  sf=0;
int  sr=0;
int  nf=0;
int  nr=0;

pthread_mutex_t mutex;
pthread_cond_t cond;

int normal_count[DOCTORS]={0};

int Critical_Size()
{
  return cr-cf;
}

int Serious_Size()
{
  return sr-sf;
}

int Normal_Size()
{
  return nr-nf;
}

void push(Patient p)
{
   if(p.type==CRITICAL)
   {
      cq[cr++%MAX]=p;
   }
   else if(p.type==SERIOUS) 
   {
     sq[sr++%MAX]=p;
   }
   else
   {
      nq[nr++%MAX]=p;
   }
}

Patient popc()
{
     return cq[cf++%MAX];
}

Patient pops()
{
   return sq[sf++%MAX];
}

Patient popn()
{
  return nq[nf++%MAX];
}

void promote_serious()
{
   if(Serious_Size() >= 5)
   {
        Patient p=pops();
        p.type=CRITICAL;
        push(p);
   }
}

void enforce_wait()
{
  time_t now=time(NULL);

  for(int tf =sf;tf<sr;tf++)
  {
    if(difftime(now,sq[tf%MAX].arrival)>=30)
    {
        Patient p = sq[tf%MAX];
        sq[tf%MAX]=sq[(--sr)%MAX];
        p.type=CRITICAL;
        push(p);
        tf--;
    }
  }

  for(int r = nf;r < nr;r++)
  {
    if(difftime(now,nq[r%MAX].arrival) >= 30)
    {
        Patient p=nq[r%MAX];
        nq[r%MAX]=nq[(--nr)%MAX]; 
        p.type=SERIOUS;
        push(p);
        r--;
    }
  }

}

void Treat(int id, Patient p)
{
  printf(" Doctor is :  %d Treaing Patient : %d Type of condition is : %d \n",id, p.id, p.type);
  sleep(1);
}

void* patient_thread(void* arg)
{
   Patient* p=(Patient*)arg;

   pthread_mutex_lock(&mutex);

   push(*p);
   promote_serious();
   pthread_cond_broadcast(&cond);

   pthread_mutex_unlock(&mutex);

   free(p);
   return NULL;
}

void* doctor_thread(void* arg)
{
   int id=((int*)arg)[0];
   DoctorType doctor =((int*)arg)[1];

   while(1)
   {
     pthread_mutex_lock(&mutex);

    while(1)
    {
        enforce_wait();
        promote_serious();

        if(doctor == SENIOR && Critical_Size() > 0)
        {
            Patient p=popc();
            pthread_mutex_unlock(&mutex);
            Treat(id,p);
            pthread_mutex_lock(&mutex);
            pthread_cond_broadcast(&cond);
            break;
        }

        if(doctor == JUNIOR && Critical_Size() > 0)
        {
            pthread_cond_wait(&cond,&mutex);
            continue;
        }

        if(normal_count[id] >= 3 && Serious_Size() == 0)
        {
            pthread_cond_wait(&cond,&mutex);
            continue;
        }

        if(normal_count[id] >= 3 && Serious_Size() > 0)
        {
            Patient p=pops();
            normal_count[id]=0;
            pthread_mutex_unlock(&mutex);
            Treat(id,p);
            pthread_mutex_lock(&mutex);
            pthread_cond_broadcast(&cond);
            break;
        }

        if(Critical_Size() > 0)
        {
            pthread_cond_wait(&cond,&mutex);
            continue;
        }

        if(Serious_Size() > 0)
        {
            Patient p=pops();
            normal_count[id]=0;
            pthread_mutex_unlock(&mutex);
            Treat(id,p);
            pthread_mutex_lock(&mutex);
            pthread_cond_broadcast(&cond);
            break;
        }

        if(Normal_Size() > 0)
        {
            Patient p=popn();
            normal_count[id]++;
            pthread_mutex_unlock(&mutex);
            Treat(id,p);
            pthread_mutex_lock(&mutex);
            pthread_cond_broadcast(&cond);
            break;
        }

        pthread_cond_wait(&cond,&mutex);  
     }

      pthread_mutex_unlock(&mutex);  
   }

}

void* monitor_thread(void* arg)
{
   while(1)
   {
        sleep(1);
        pthread_mutex_lock(&mutex);
        enforce_wait();
        promote_serious();
        pthread_cond_broadcast(&cond);
        pthread_mutex_unlock(&mutex);
   }
}

int main()
{
   pthread_mutex_init(&mutex,NULL);
   pthread_cond_init(&cond,NULL);

   pthread_t doc[DOCTORS];
   pthread_t pat[20];
   pthread_t monitor;

   int args[DOCTORS][2]=
   {
    {0,SENIOR},{1,SENIOR},
    {2,JUNIOR},{3,JUNIOR}
   };


   for(int doctor = 0;doctor < DOCTORS;doctor++)
   {
     pthread_create(&doc[doctor],NULL,doctor_thread,args[doctor]);
   }

   pthread_create(&monitor,NULL,monitor_thread,NULL);

   for(int i=0;i<20;i++)
   {
     Patient* p=malloc(sizeof(Patient));
     p->id=i;
     p->type=rand() % 3;
     p->arrival=time(NULL);

    pthread_create(&pat[i],NULL,patient_thread,p);
    sleep(1);
   }

   for(int i=0;i<20;i++)
   {
     pthread_join(pat[i],NULL);
   }

   return 0;

}
