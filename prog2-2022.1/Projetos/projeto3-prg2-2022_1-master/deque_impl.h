//
// Created by wagner on 22/07/22.
//

#ifndef PROJETO_3_WAGNER_DEQUE_IMPL_H
#define PROJETO_3_WAGNER_DEQUE_IMPL_H

namespace prg2{

    template <typename T> trecho<T> * trecho_cria(int tam_trecho){
        auto p_trecho = new trecho<T>;

        //inicia um fila para que tenha uma certa capacidade
        p_trecho->fila= fila_cria<T>(tam_trecho);
        p_trecho->proximo = nullptr;

        return p_trecho;

    }

    //as operações do deque

    //cria um deque vazio
    template <typename T> deque <T> deque_cria(int tam_trecho){
        deque<T>q;

        auto p_trecho = trecho_cria<T>(tam_trecho);

        q.tamanho=0;
        q.primeiro = p_trecho;
        q.ultimo = p_trecho;

        return q;
    }

    //destroi um deque
    template <typename T> void deque_destroi(deque <T> & q){

    }

    //retorna o tamanho do deque
    template <typename T> int  deque_tamanho(const deque <T> & q){
        return q.tamanho;
    }

    //testa se o deque esta vazio
    template <typename T> bool  deque_vazio(const deque <T> & q){
        return q.tamanho == 0;
    }

    //acrescenta um dado ao final do deque
    template <typename T> void  deque_anexa(deque <T>q, const T & dado){
        //se a fila do ultimo trecho estiver cheia
        //expande o deque
        if(fila_cheia(q.ultimo->fila)){
            auto n = fila_tamanho(q.ultimo->fila);
            q.ultimo->proximo = trecho_cria<T>(n);
            q.ultimo=q.ultimo->proximo;
        }
        //anexa dado no final do ultimo trecho
        fila_anexa(q.ultimo->fila,dado);
        q.tamanho++;

    }

    //acrescenta um dado ao inicio do deque
    template <typename T> void  deque_insere(deque <T>q, const T & dado){
        if(fila_insere(q.primeiro->fila,dado));
        else {
            int tam = fila_tamanho(q.primeiro->fila);
            auto p = trecho_cria<T>(tam);
            p->proximo = q.primeiro;
            q.primeiro = p;
            fila_insere(q.primeiro->fila, dado);
        }
        q.tamanho;

    }

    //remove um dado ao final do deque
    //se pos for inválido, dispara uma excessão invalid_argumente
    template <typename T> void  deque_remove_final(deque <T> & q){

    }

    //remove um dado ao inicio do deque
    //se pos for inválido, dispara uma excessão invalid_argumente
    template <typename T> void  deque_remove_inicio(deque <T> & q){

    }

    //acessa um dado ao final do deque
    //se pos for inválido, dispara uma excessão invalid_argumente
    template <typename T> T&  deque_acessa_final(deque <T> & q){
        if(deque_vazio(q)){
            throw std::invalid_argument("deque vazio");
        }
        return fila_atras(q.ultimo->fila);

    }


    //acessa um dado ao inicio do dequeb v
    //se pos for inválido, dispara uma excessão invalid_argumente
    template <typename T> T&  deque_acessa_inicio(deque <T> & q){
        if(deque_vazio(q)){
            throw std::invalid_argument("deque vazio");
        }
        return fila_frente(q.primeiro->fila);

    }

    //acessa um dado de uma posição qualquer
    //se pos for inválido, dispara uma excessão invalid_argumente
    template <typename T> T&  deque_acessa(deque <T> & q, int pos){

    }

}
#endif //PROJETO_3_WAGNER_DEQUE_IMPL_H
