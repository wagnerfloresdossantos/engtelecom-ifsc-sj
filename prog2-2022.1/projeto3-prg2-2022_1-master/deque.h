//
// Created by wagner on 22/07/22.
//

#ifndef PROJETO_3_WAGNER_DEQUE_H
#define PROJETO_3_WAGNER_DEQUE_H
#include "fila_circular.h"
#include "sistema.h"

// a definição da API do deque !
namespace prg2 {
    //a declaração do tipo deque
    //ainda incompleta!
    template<typename T> struct trecho{
        //contem uma fila circular e um ponteiro
        //para próximo trecho
        fila_circular <T>fila;
        trecho<T> * proximo;
    };
    template <typename T> struct deque{
        //uma sequencia de uma ou mais filas circulares
        trecho<T> * primeiro, * ultimo;

        int tamanho;
    };

    //as operações do deque

    const int tam_default=16;

    //cria um deque vazio
    template <typename T> deque <T> deque_cria(int tam_trecho=tam_default);

    //destroi um deque
    template <typename T> void deque_destroi(deque <T> & q);

    //retorna o tamanho do deque
    template <typename T> int  deque_tamanho(const deque <T> & q);

    //testa se o deque esta vazio
    template <typename T> bool  deque_vazio(const deque <T> & q);

    //acrescenta um dado ao final do deque
    template <typename T> void  deque_anexa(deque <T>, const T & dado);

    //acrescenta um dado ao inicio do deque
    template <typename T> void  deque_insere(deque <T>, const T & dado);

    //remove um dado ao final do deque
    //se pos for inválido, dispara uma excessão invalid_argumente
    template <typename T> void  deque_remove_final(deque <T> & q);

    //remove um dado ao inicio do deque
    //se pos for inválido, dispara uma excessão invalid_argumente
    template <typename T> void  deque_remove_inicio(deque <T> & q);

    //acessa um dado ao final do deque
    //se pos for inválido, dispara uma excessão invalid_argumente
    template <typename T> T&  deque_acessa_final(deque <T> & q);

    //acessa um dado ao inicio do deque
    //se pos for inválido, dispara uma excessão invalid_argumente
    template <typename T> T&  deque_acessa_inicio(deque <T> & q);

    //acessa um dado de uma posição qualquer
    //se pos for inválido, dispara uma excessão invalid_argumente
    template <typename T> T&  deque_acessa(deque <T> & q, int pos);

}
#include "deque_impl.h"
#endif //PROJETO_3_WAGNER_DEQUE_H
