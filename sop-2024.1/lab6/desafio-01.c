/*
Desafio 1: Considere o desenvolvimento de um sistema que simule um  estacionamento no qual:

    O número de vagas neste estacionamento possui limite de 10 e inicia vazio;
    Existem 7 cancelas de entrada;
    Têm-se 20 carros chegando aleatoriamente em qualquer uma das 7 cancelas "ao mesmo tempo";
    A passagem de um carro pela cancela leva 5 segundos e nenhum carro pode entrar pela mesma enquanto um carro está em passagem;
    Uma vez estacionado o carro deve sair em tempo entre 10 e 20 segundos;
    Você deve numerar os carros por ordem de chegada independente de cancela;
    Imprima:

    Quando um carro X chega em uma cancela Y;
    Quando o carro X começa a entrar pela cancela Y;
    Quando o carro X deixa o estacionamento.

Obs1: Note que os carros irão entrar por ordem de chegada, independente de em qual cancela estejam.
Obs2: Note que podem haver cancelas sem carros na fila de entrada e fila maior em outras cancelas.
*/


#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <semaphore.h>
#include <unistd.h>

#define NUM_CARROS 20

sem_t s;
int num = 0;
pthread_mutex_t mutex_num;
pthread_mutex_t mutex_cancela[7];

void *carroEstacionando(void *)
{
    int cancela;
    int meu_num;
    
    pthread_mutex_lock (&mutex_num);
    num++;
    meu_num = num;
    pthread_mutex_unlock (&mutex_num);   
    
    cancela = rand() % 7;
    
    printf("Carro %d chegou na cancela %d\n", meu_num, cancela);

    sem_wait(&s);
    
    pthread_mutex_lock(&mutex_num);
    printf("Carro %d entrando na cancela %d\n", meu_num, cancela);
    sleep(5);
    pthread_mutex_unlock(&mutex_num);
    sleep(10+rand()%10);
    
    sem_post(&s);

    printf("carro %d saindo\n", meu_num);

    pthread_exit(NULL);
        
}


int main (int argc, char *argv[])
{

    pthread_t carro[NUM_CARROS];
    pthread_attr_t attr;
    long status;

    sem_init(&s,0,10);
    pthread_mutex_init(&mutex_num, NULL);

    for (int i = 0; i < 7; i++)
    {
        pthread_mutex_init(&mutex_cancela[i],NULL);
    }

    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);

    for(int i=0;i<NUM_CARROS; i++)
    {
        status = pthread_create(&carro[i],&attr,carroEstacionando, NULL);
        if (status){
            perror("phtread_join");
            exit(1);
        }
    }

    pthread_attr_destroy(&attr);

    for (int i = 0; i < NUM_CARROS; i++)
    {
        pthread_join(carro[i], NULL);
    }

    pthread_exit(NULL);
}