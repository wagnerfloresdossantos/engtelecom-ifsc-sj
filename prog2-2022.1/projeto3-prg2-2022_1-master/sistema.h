


#ifndef PROJETO_3_WAGNER_SISTEMA_H
#define PROJETO_3_WAGNER_SISTEMA_H

#include <iostream>
#include <fstream>
#include "errno.h"
#include <list>
#include <string.h>
#include <iomanip>

using namespace std;
//struct
struct classe{
    //Elementos obtidos do arquivo csv
    string data;
    double valor;

};

list<classe> leitura_csv(ifstream & arq);

void mms(list<classe> & classes, int periodo);

void mmp(list<classe> & classes, int periodo);

void mmp_deque(list<classe> & classes, int periodo);

#endif //PROJETO_3_WAGNER_SISTEMA_H
