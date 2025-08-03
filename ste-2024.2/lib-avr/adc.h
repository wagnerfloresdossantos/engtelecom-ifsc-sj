#ifndef __ADC_H__
#define __ADC_H__

#include "fifo.h"

class ADC_Channel
{
public:
    // Construtor: Inicializa o ADC e configura o canal
    enum ADC_Channel_t {
        ADC_Channel_0 = 0,
        ADC_Channel_1,
        ADC_Channel_2,
        ADC_Channel_3,
        ADC_Channel_4,
        ADC_Channel_5,
        ADC_Channel_6,
        ADC_Channel_7,
        ADC_Channel_1v1 = 0xc,
        ADC_Channel_0v = 0xf
    };

    enum ADC_Ref_t {
        ADC_AREF = 0,
        ADC_AVCC = 1,
        ADC_Int1v1 = 3
    };

    ADC_Channel(ADC_Channel_t ch = ADC_Channel_0, ADC_Ref_t ref = ADC_AVCC);

    // Operação por polling
    int sample();

    // Operação por interrupção
    void start(); // troca canal de ADC
    void adc_isr_handler(); // enfilera
    int get(); // retorna da fifo
    ADC_Channel *instance(int n) { return instances[n]; }
    int available() { return fifo.available(); }

private:
    static ADC_Channel instances[16];
    Fifo<int, 8> fifo;
    ADC_Channel_t channel;
    ADC_Ref_t reference;
};

#endif
