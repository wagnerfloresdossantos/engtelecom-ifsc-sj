//
// Created by wagner on 22/07/22.
//

#ifndef PROJETO_3_WAGNER_FILA_CIRCULAR_H
#define PROJETO_3_WAGNER_FILA_CIRCULAR_H

// a definição da fila circular, que é usada pelo deque !
namespace prg2 {

    template <typename T> struct fila_circular {
        T * area; //aqui sera o vetor
        int inicio,fim;
        int n; //quantidade de dados armazenados
        int capacidade; //capacidade do vetor
    };
    //cria uma fila com capacidade dada por "capacidade"
    //se "capacidade" <=0, dispara um excessão
    template <typename T> fila_circular<T> fila_cria( int capacidade);

    //destroi a fila
    template <typename T> void fila_destroi(fila_circular<T> & fila);

    //acrescenta um dado no final da fila
    template <typename T> void fila_anexa(fila_circular<T> & fila, const T & dado);

    //acrescenta um dado no inicio da fila
    template <typename T> void fila_insere(fila_circular<T> & fila, const T & dado);

    //remove um dado do final da fila
    template <typename T> void fila_remove_final(fila_circular<T> & fila);

    //remove um dado do inicio da fila
    template <typename T> void fila_remove_inicio(fila_circular<T> & fila);

    // acessa um dado na psição "pos"
    template <typename T> void fila_acessa(fila_circular<T> & fila, int pos);

    //acessa um dado da fente da fila
    template <typename T> void fila_frente(fila_circular<T> & fila);

    //acessa um dado de tras da fila
    template <typename T> void fila_atras(fila_circular<T> & fila);

    //testa se a fila esta vazia
    template <typename T> void fila_vazia(const fila_circular<T> & fila);

    //testa se a fila esta cheia
    template <typename T> void fila_cheia(const fila_circular<T> & fila);

    //retorna a quantidade de dados contidos na fila
    template <typename T> void fila_tamanho(const fila_circular<T> & fila);

}

#include "fila_circular_impl.h"
#endif //PROJETO_3_WAGNER_FILA_CIRCULAR_H
