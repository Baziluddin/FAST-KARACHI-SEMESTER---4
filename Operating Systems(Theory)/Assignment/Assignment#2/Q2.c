#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>

#define N 1000
#define M 4
#define TILE 100
#define MAX_THREADS 8
#define T_HOT 35.0
#define T_COLD -10.0

double satellites[M][N][N];
double global_mat[N][N];
double normalized[N][N];
double risk[N][N];

int is_hot[N][N]={0};
int is_cold[N][N]={0};

int hotspot_count=0;
int coldspot_count=0;
int anomaly_count=0;

pthread_mutex_t lock;
pthread_cond_t cond;

int done_hot=0;
int done_cold=0;
int done_norm=0;

typedef struct{
    int sr,er,sc,ec;
}Tile;

typedef struct{
    double val;
    int i,j;
}RiskCell;

Tile tiles[(N/TILE)*(N/TILE)];
int tile_index=0;

double global_sum=0;
double global_sq=0;
double global_min=1e9;
double global_max=-1e9;
int total_count=0;

int risk_tile_index=0;

void interpolate(double mat[N][N])
{
    for(int i=0;i<N;i++)
    {
        for(int j=0;j<N;j++)
        {
            if(isnan(mat[i][j]))
            {
                double sum=0;
                int c=0;

                if(i > 0 && !isnan(mat[i-1][j]))
                {
                   sum+=mat[i-1][j];
                   c++;

                }

                if(i < N-1 && !isnan(mat[i+1][j]))
                {
                   sum+=mat[i+1][j];
                   c++;

                }

                if(j > 0 && !isnan(mat[i][j-1]))
                {
                   sum+=mat[i][j-1];
                   c++;

                }

                if(j < N-1 && !isnan(mat[i][j+1]))
                {
                    sum+=mat[i][j+1];
                    c++;
                }

                mat[i][j]= c? sum/c : 0;
            }
        }
    }
}


void* sat_thread(void* arg)
{
    int id = *(int*)arg;
    interpolate(satellites[id]);
    return NULL;
}

void* merge_worker(void* arg)
{
    int id = *(int*)arg;
    int rows = N / MAX_THREADS;
    int s = id * rows;
    int e = (id == MAX_THREADS-1)?N:s+rows;

    for(int i=s;i<e;i++)
    {
        for(int j=0;j<N;j++)
        {
            double sum=0;
            int c=0;

            for(int k=0 ;k<M ;k++)
            {
                if(!isnan(satellites[k][i][j]))
                {
                    sum+=satellites[k][i][j];
                    c++;
                }
            }

            global_mat[i][j]= c? sum/c : 0;
        }
    }

    return NULL;
}


void* tile_worker(void* arg)
{
    while(1)
    {
        pthread_mutex_lock(&lock);

        if(tile_index >= (N/TILE)*(N/TILE))
        {
            pthread_mutex_unlock(&lock);
            break;
        }

        Tile t = tiles[tile_index++];
        pthread_mutex_unlock(&lock);

        double sum=0;
        double sq=0;
        double min=1e9;
        double max=-1e9;

        int count=0;

        for(int i=t.sr ;i<t.er ;i++)
        {
            for(int j=t.sc ;j<t.ec ;j++)
            {
                double v=global_mat[i][j];
                sum+=v;
                sq+=v*v;

                if(v<min)
                {
                    min=v;
                }

                if(v>max)
                {
                    max=v;
                }

                count++;
            }
        }

        double mean=sum/count;
        double var_local=(sq/count)-(mean*mean);
        if(var_local<0)
        {
            var_local=0;
        }

        double std=sqrt(var_local);

        int local_anom=0;
        for(int i=t.sr ;i<t.er ;i++)
        {
            for(int j=t.sc ;j<t.ec ;j++)
            {
                if(fabs(global_mat[i][j]-mean) > 2*std)
                {
                    local_anom++;
                }
            }
        }

        pthread_mutex_lock(&lock);
        anomaly_count+=local_anom;
        global_sum+=sum;
        global_sq+=sq;
        total_count+=count;

        if(min<global_min)
        {
              global_min=min;
        }

        if(max>global_max)
        {
              global_max=max;
        }

        pthread_mutex_unlock(&lock);
    }

    return NULL;
}


double proximity_hot(int i,int j)
{
    double min_d=1e9;
    for(int x=-2;x<=2;x++)
    {
        for(int y=-2;y<=2;y++)
        {
            if(abs(x)+abs(y)<=2)
            {
                int ni=i+x,nj=j+y;
                if(ni >= 0 && nj >= 0 && ni < N && nj < N && is_hot[ni][nj])
                {
                    double d=abs(x)+abs(y);
                    if(d<min_d)
                    {
                         min_d=d;
                    }
                }
            }
        }
    }

    return (min_d<1e9) ? 1.0/(min_d+1):0;

}

double proximity_cold(int i,int j)
{
    double min_d=1e9;
    for(int x=-2;x<=2;x++)
    {
        for(int y=-2;y<=2;y++)
        {
            if(abs(x)+abs(y)<=2)
            {
                int ni=i+x,nj=j+y;
                if(ni >= 0 && nj >= 0 && ni < N && nj < N && is_cold[ni][nj])
                {
                    double d=abs(x)+abs(y);
                    if(d<min_d)
                    {
                         min_d=d;
                    }
                }
            }
        }
    }

    return (min_d<1e9) ? 1.0/(min_d+1):0;
}

void* taskA(void* arg)
{
    int local=0;
    for(int i=0;i<N;i++)
    {
        for(int j=0;j<N;j++)
        {
            if(global_mat[i][j] > T_HOT)
            {
                pthread_mutex_lock(&lock);
                is_hot[i][j]=1;
                hotspot_count++;
                pthread_mutex_unlock(&lock);
                local++;
            }
        }
    }
    pthread_mutex_lock(&lock);
    done_hot=1;
    pthread_cond_broadcast(&cond);
    pthread_mutex_unlock(&lock);
    return NULL;
}


void* taskB(void* arg)
{
    int local=0;
    for(int i=0;i<N;i++)
    {
        for(int j=0;j<N;j++)
        {
            if(global_mat[i][j] < T_COLD)
            {
                pthread_mutex_lock(&lock);
                is_cold[i][j]=1;
                coldspot_count++;
                pthread_mutex_unlock(&lock);
                local++;
            }
        }
    }
    pthread_mutex_lock(&lock);
    done_cold=1;
    pthread_cond_broadcast(&cond);
    pthread_mutex_unlock(&lock);
    return NULL;
}


void* taskC(void* arg)
{
    pthread_mutex_lock(&lock);
    while(!(done_hot && done_cold))
    {
        pthread_cond_wait(&cond,&lock);
    }

    pthread_mutex_unlock(&lock);

    double min=global_min;
    double max=global_max;

    for(int i=0;i<N;i++)
    {
        for(int j=0;j<N;j++)
        {
            double v=global_mat[i][j];
            double ph=proximity_hot(i,j);
            double pc=proximity_cold(i,j);

            if(ph>0 && pc>0)
            {
               v+=(ph+pc);
            }

            if(max==min)
            {
                 normalized[i][j]=0;
            }

            else
            {
                normalized[i][j]=(v-min)/(max-min);
            }
        }
    }

    pthread_mutex_lock(&lock);
    done_norm=1;
    pthread_cond_broadcast(&cond);
    pthread_mutex_unlock(&lock);
    return NULL;
}


void* risk_thread(void* arg)
{
    pthread_mutex_lock(&lock);
    while(!(done_hot && done_cold && done_norm))
    {
        pthread_cond_wait(&cond,&lock);
    }
    pthread_mutex_unlock(&lock);

    while(1)
    {
        pthread_mutex_lock(&lock);
        if(risk_tile_index >= (N/TILE)*(N/TILE))
        {
            pthread_mutex_unlock(&lock);
            break;
        }

        Tile t = tiles[risk_tile_index++];
        pthread_mutex_unlock(&lock);

        for(int i=t.sr;i<t.er;i++)
        {
            for(int j=t.sc;j<t.ec;j++)
            {
                double ph=proximity_hot(i,j);
                double pc=proximity_cold(i,j);
                risk[i][j]=normalized[i][j]*ph/(pc+1);
            }
        }
    }
    return NULL;
}


int main()
{
    pthread_mutex_init(&lock,NULL);
    pthread_cond_init(&cond,NULL);

    for(int k=0;k<M;k++)
    {
        for(int i=0;i<N;i++)
        {
            for(int j=0;j<N;j++)
            {
                satellites[k][i][j]=(rand()%20==0)?NAN:(rand()%50);
            }
        }
    }

    pthread_t sat[M]; 
    int ids[M];
    for(int i=0;i<M;i++)
    {
        ids[i]=i;
        pthread_create(&sat[i],NULL,sat_thread,&ids[i]);
    }

    for(int i=0;i<M;i++)
    {
       pthread_join(sat[i],NULL);
    }

    pthread_t merge_t[MAX_THREADS]; 
    int mid[MAX_THREADS];

    for(int i=0;i<MAX_THREADS;i++)
    {
        mid[i]=i;
        pthread_create(&merge_t[i],NULL,merge_worker,&mid[i]);
    }

    for(int i=0;i<MAX_THREADS;i++)
    {
         pthread_join(merge_t[i],NULL);
    }

    int idx=0;
    for(int i=0;i<N;i+=TILE)
    {
        for(int j=0;j<N;j+=TILE)
        {
            tiles[idx++]=(Tile){i,(i+TILE>N?N:i+TILE),j,(j+TILE>N?N:j+TILE)};
        }
    }

    pthread_t w[MAX_THREADS];
    for(int i=0;i<MAX_THREADS;i++)
    {
        pthread_create(&w[i],NULL,tile_worker,NULL);
    }

    for(int i=0;i<MAX_THREADS;i++)
    {
        pthread_join(w[i],NULL);
    }

    pthread_t A,B,C;
    pthread_create(&A,NULL,taskA,NULL);
    pthread_create(&B,NULL,taskB,NULL);
    pthread_create(&C,NULL,taskC,NULL);

    pthread_t R[MAX_THREADS];

    for(int i=0;i<MAX_THREADS;i++)
    {
        pthread_create(&R[i],NULL,risk_thread,NULL);
    }

    pthread_join(A,NULL);
    pthread_join(B,NULL);
    pthread_join(C,NULL);
    for(int i=0;i<MAX_THREADS;i++)
    {
           pthread_join(R[i],NULL);
    }

    double mean=global_sum/total_count;
    double var=(global_sq/total_count)-mean*mean;
    double std=sqrt(var);

    printf(" Max of : %f  and Min of : %f and Mean of :%f and  Var of :%f and Std of : %f\n",global_max,global_min,mean,var,std);
    printf("Hot:%d , Cold:%d , Anomaly:%d \n",hotspot_count,coldspot_count,anomaly_count);
    printf("\n");
    printf("Sample normalized matrix:\n");
    for(int i=0;i<5;i++)
    {
        for(int j=0;j<5;j++)
        {
            printf("%.2f ",normalized[i][j]);
        }
        printf("\n");
    }

    RiskCell top[10];
    for(int i=0;i<10;i++)
    {
     top[i].val=-1;
    }

    for(int i=0;i<N;i++)
    {
        for(int j=0;j<N;j++)
        {
            double v=risk[i][j];
            for(int k=0;k<10;k++)
            {
                if(v>top[k].val)
                {
                    for(int x=9;x>k;x--) top[x]=top[x-1];
                    top[k]=(RiskCell){v,i,j};
                    break;
                }
            }
        }
    }
    
    printf("\n");

    printf(" Top 10 risk cells:\n");
    for(int i=0;i<10;i++)
    {
        printf(" [%d,%d] :  %f\n",top[i].i,top[i].j,top[i].val);
    }

    return 0;
}
