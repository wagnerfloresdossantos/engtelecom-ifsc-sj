//
// Created by wagner on 22/07/22.
//

#ifndef PROJETO_3_WAGNER_FILA_CIRCULAR_IMPL_H
#define PROJETO_3_WAGNER_FILA_CIRCULAR_IMPL_H

namespace prg2{

    int incremento_circular(int pos, int capacidade){
        pos++;
        if (pos == capacidade) pos = 0;
        return pos;
    }

    int decremento_circular(int pos, int capacidade){
        if (pos == 0){
            pos = capacidade-1;
        }else {
            pos --;
        }
        return pos;
    }

    template <typename T> fila_circular<T> fila_cria( int capacidade){
        //verifica se a capacidade é válida
        if(capacidade <=0){
            throw std::invalid_argument("capacidade deve ser > 0");
        }
        fila_circular<T>fila;

        fila.inicio = 0;
        fila.fim = 0;
        fila.n = 0;
        fila.capacidade = capacidade;
        //aloca memoria
        fila.area = new T [capacidade];

        return fila;

    }

    template <typename T> void fila_destroi(fila_circular<T> & fila){
        //libera memoria
        delete[] fila.area;
        fila.area = nullptr;
        fila.inicio = 0;
        fila.fim = 0;
        fila.n = 0;
        fila.capacidade = 0;

    }

    //acrescenta um dado no final da fila
    template <typename T> void fila_anexa(fila_circular<T> & fila, const T & dado){
        if(fila_cheia(fila)){
            throw std::invalid_argument("fila cheia");
        }
        fila.area[fila.fim] = dado;
        fila.n++; // incrementa a qtd de dados armazenados
        fila.fim++;

        fila.fim = incremento_circular(fila.fim,fila.capacidade);
    }

    //acrescenta um dado no inicio da fila
    template <typename T> void fila_insere(fila_circular<T> & fila, const T & dado) {
        if (fila_cheia(fila)) {
            throw std::invalid_argument("fila cheia");
        }
        //decremento circular
        fila.inicio = decremento_circular(fila.inicio,fila.capacidade);
        fila.area[fila.inicio]=dado;
        fila.n++;
    }

    template <typename T> void fila_remove_final(fila_circular<T> & fila){
        if (fila_vazia(fila)) {
            throw std::invalid_argument("fila vazia");
        }
        fila.fim = decremento_circular(fila.fim,fila.capacidade);
        fila.n--;

    }

    template <typename T> void fila_remove_inicio(fila_circular<T> & fila){
        if (fila_cheia(fila)) {
            throw std::invalid_argument("fila cheia");
        }
        fila.inicio = incremento_circular(fila.inicio,fila.capacidade);
        fila.n--;
    }

    template <typename T> void fila_acessa(fila_circular<T> & fila, int pos){
        if (fila_vazia(fila)) {
            throw std::invalid_argument("fila vazia");
        }
        if(pos >=fila.n){
            throw std::invalid_argument("posição invalida");
        }
        pos = (fila.inicio + pos) % fila.capacidade;
        return fila.area[pos];
    }

    template <typename T> void fila_frente(fila_circular<T> & fila){
        if (fila_vazia(fila)) {
            throw std::invalid_argument("fila vazia");
        }
        return fila.area[fila.inicio];
    }

    template <typename T> void fila_atras(fila_circular<T> & fila){
        if (fila_vazia(fila)) {
            throw std::invalid_argument("fila vazia");
        }
        auto pos = decremento_circular(fila.fim,fila.capacidade);
        return fila.area[fila.pos];
    }

    template <typename T> bool fila_vazia(const fila_circular<T> & fila){
        return fila.n == 0;
    }

    template <typename T> bool fila_cheia(const fila_circular<T> & fila){
        return fila.n == fila.capacidade;
    }

    template <typename T> int fila_tamanho(const fila_circular<T> & fila){
        return fila.n;
    }
}

#endif //PROJETO_3_WAGNER_FILA_CIRCULAR_IMPL_H
