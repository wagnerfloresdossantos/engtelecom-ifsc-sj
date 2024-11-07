#include "sistema.h"

//Função que separa uma linha baseada em um caracter passado para a mesma
list<string> separa(const string &texto, const string &sep) {

    //declara uma variável temporaria para devolver o resultado como lista
    list<string> lista;

    //caso não tenha nada dentro do texto , devolve uma lista vazia
    if (!texto.empty()) {
        //Variavel pos = posições do character separa
        //Variavel coisa = Copia de algo que está declarada como constante
        int pos = 0;
        string coisa = texto;

        //loop que separa a string
        //pos recebe a posição do character 'sep'
        //Coloca a substring de 0 até pos dentro da fila
        //Apaga a substring utilizada
        while (pos != string::npos) {
            pos = coisa.find(sep);
            lista.push_back(coisa.substr(0, pos));
            coisa.erase(0, pos + 1);
        }
    }
    return lista;

}
//Funçao que cria classe temporaria e armazena na struct classe
classe cria_classe(const list<string> & lista)
{
    //A lista está ordenada da mesma forma que o arquivo
    //Primeiro código da classe
    classe classe_temporario;
    //adiciona data na classe data
    classe_temporario.data = lista.front();
    //adiciona volor na classe valor
    classe_temporario.valor = stod(lista.back());
    //retorna classe temporaria
    return classe_temporario;
}

//Função Leitura do arquivo csv
list<classe> leitura_csv(ifstream & arq ){
    //Lista onde Todas as classes passadas pelo arquivo vão ser armazenadas
    //String linha para a leitura das linhas do arquivo
    list<classe> temp_classes;
    string linha;

    //Enquanto é possivel ler uma linha desse arquivo ele repete o loop
    while (getline(arq, linha)) {

        //Declaração de Lista temporaria e de classe temporaria
        //lista temporaria que contem os dados de uma linha do arquivo
        //classe_de_clientes temporaria os quais serão armazenados dentro da fila de classes
        list<string> lista_temporaria = separa(linha, " ");
        classe classe_temporaria;
        //Chama o adiona_a_classe que converte os dados que estão na lista em uma classe_temporaria
        //Logo em seguida pega a classe_temporaria e armazena em uma lista com todas as classes
        temp_classes.push_back(cria_classe(lista_temporaria));
    }
    return temp_classes;
}

//funçao grafica que mostra o resultado na tela
void mostra_tela(list<string> & lista){
    //laço que percorre a lista
    for(auto &y:lista){
        //variavel que localiza o espaço
        int  pos =  y.rfind(' ');
        //mostra na tela data que vem antes do espaço, reduz o tamanho da media para tamanho 4 mostra o valor
        cout <<  y.substr(pos+1,y.size()) << " " << fixed << setprecision(2) << stod(y.substr(0,pos)) << endl;
    }
}

//funçao que calcula a media movel simples
void mms(list<classe> & classes, int periodo) {
    //lista temporária com os valores a serem mostrados
    list<string> lista_temp;
    //laço que percorre a lista de classes
    for (auto it = classes.begin(); it != classes.end(); it++) {
        //retorna o laço para a primiera posiçao da lista
        it = classes.begin();
        //variavel para numerador da conta
        double numerador = 0;
        //laço que percorre o periodo selecionado via argv[2]
        for (int i = 0; i < periodo; i++) {
            //faz o calculo de soma do numerador
            numerador += it->valor;
            //faz a interaçao da variavel it
            it++;
        }
        //decrementa a interaçao da variavel it para que o ultimo valor apareça na tela
        it--;
        //adiciona a lista uma string com o calulo e data
        lista_temp.push_back(to_string(numerador / periodo)+" "+( it->data));
        //retira o primeiro item da lista de classes
        classes.pop_front();
    }
    //chama a funçao que apresenta na tela o resultado
    mostra_tela(lista_temp);
}
//funçao que calcula a media movel ponderada
void mmp(list<classe> & classes, int periodo) {
    //lista temporária com os valores a serem mostrados
    list<string> lista_temp;
    //laço que percorre a lista de classes
    for (auto it = classes.begin(); it != classes.end(); it++) {
        //retorna o laço para a primiera posiçao da lista
        it = classes.begin();
        //variavel para numerador da conta
        double numerador = 0;
        //variavel para denominador da conta
        double denominador=0;
        //laço que percorre o periodo programado via argv[2]
        for (int i = 0; i < periodo; i++) {
            //faz o calculo de soma donominador
            numerador += it->valor * (i + 1);
            //faz o calculo de soma do denominador
            denominador += (i+1);
            //incrementa a lista
            it++;
        }
        //decrementa a lista para mostrar o ultimo valor
        it--;
        //adiciona a lista temporaria a media e a data
        lista_temp.push_back(to_string(numerador / denominador)+" "+( it->data));
        //retira o primeiro item da lista de classes
        classes.pop_front();
    }
    //chama a funçao grafica
    mostra_tela(lista_temp);
}


//funçao que calcula a media movel ponderada
void mmp_deque(list<classe> & classes, int periodo) {
    //lista temporária com os valores a serem mostrados
    list<string> lista_temp;
    //laço que percorre a lista de classes
    for (auto it = classes.begin(); it != classes.end(); it++) {
        //retorna o laço para a primiera posiçao da lista
        it = classes.begin();
        //variavel para numerador da conta
        double numerador = 0;
        //variavel para denominador da conta
        double denominador=0;
        //laço que percorre o periodo programado via argv[2]
        for (int i = 0; i < periodo; i++) {
            //faz o calculo de soma donominador
            numerador += it->valor * (i + 1);
            //faz o calculo de soma do denominador
            denominador += (i+1);
            //incrementa a lista
            it++;
        }
        //decrementa a lista para mostrar o ultimo valor
        it--;
        //adiciona a lista temporaria a media e a data
        lista_temp.push_back(to_string(numerador / denominador)+" "+( it->data));
        //retira o primeiro item da lista de classes
        classes.pop_front();
    }
    //chama a funçao grafica
    mostra_tela(lista_temp);
}