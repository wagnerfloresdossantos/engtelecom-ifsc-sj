#include <iostream>
#include <fstream>
#include "errno.h"
#include <list>
#include <iomanip>
#include "sistema.h"
#include "deque.h"
#include "fila_circular_impl.h"
#include "deque_impl.h"

using namespace std;


string deque2string(prg2::deque<int> & q, char delim=',') {
    string r;

    // somente gera a string de resultado se deque não estiver vazio
    if (! prg2::deque_vazio(q)) {
        auto len = prg2::deque_tamanho(q);
        // itera o deque, convertendo seus valores para string e unindo-os com o caractere delim
        for (int j = 0; j < len; j++) {
            r += std::to_string(prg2::deque_acessa(q, j)) + delim;
        }
        // remove o caractere delimitador em excesso
        r.pop_back();
    }

    return r;
}

int main(int argc, char **argv) {
    //Verifica se os argumentos de linha são suficientes
    if (argc <= 3) {
        perror("Falta argumento na linha de comando!sera apresentada a Media Movel Simples");
    }

    //Abre o arquivo
    ifstream arq(argv[1]);

    //Caso o arquivo não abra
    if (!arq.is_open()) {
        perror("Erro ao abrir o Arquivo!");
    }

    //cria a variavel inteiro intervalo a ser informado por argv[2]
    int intervalo = stoi(argv[2]);

    //cria a variavel string tipo que vai definir o tipo de mdia a ser apurada informada por arv[3]
    string tipo;
    if (argc > 3) {
        tipo = argv[3];
    }
    // cria um deque que armazena int
    auto q = prg2::fila_cria<int> (4);
    // cria um deque que armazena int
    auto q1 = prg2::deque_cria<int>();

    //adiciona a lista de classes os dados do arquivo CSV
    list<classe>classes = leitura_csv(arq);
    //se for selecionado via argv[3] mms ou em branco, chama a funçao Media Movel Simples
    if(tipo == "mms" || tipo.empty()) {
        //chama a função que calcula a media movel simples
        mms(classes, intervalo);
    //senao chama a Media Movel Ponderada
    }else {
        //chama a função quelcula a media movel ponderada
        mmp(classes, intervalo);
        //chama a função quelcula a media movel ponderada
//        mmp_deque(classes, intervalo);
    }

}

