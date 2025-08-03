#include "adc.h"
#include <avr/io.h>
#include <avr/interrupt.h>



// Definição das instâncias estáticas
ADC_Channel ADC_Channel::instances[16];

// Construtor: Configura o canal e referência
ADC_Channel::ADC_Channel(ADC_Channel_t ch, ADC_Ref_t ref)
    : channel(ch), reference(ref)
{
    // Configurar a referência de tensão e alinhar à direita (ADLAR = 0)
    ADMUX = (reference << REFS0);

    // Configurar o prescaler para 128, habilitar o ADC e interrupção
    ADCSRA = (1 << ADEN) | (1 << ADIE) | 0x07;

    // Salvar a instância do canal
    instances[ch] = *this;
}

// Método síncrono: Faz uma única amostragem do canal
int ADC_Channel::sample()
{
    // Configurar o canal
    ADMUX = (ADMUX & 0xF0) | (channel & 0x0F);

    // Iniciar a conversão
    ADCSRA |= (1 << ADSC);

    // Aguardar conclusão da conversão
    while (ADCSRA & (1 << ADSC));

    // Retornar o valor convertido (10 bits)
    return ADCW;
}

// Método assíncrono: Inicia uma conversão no canal
void ADC_Channel::start()
{
    // Configurar o canal
    ADMUX = (ADMUX & 0xF0) | (channel & 0x0F);

    // Iniciar a conversão
    ADCSRA |= (1 << ADSC);
}

// Manipulador de interrupção do ADC
void ADC_Channel::adc_isr_handler()
{
    // Adicionar valor convertido à FIFO
    fifo.put(ADCW);

    // Iniciar uma nova conversão automaticamente
    ADCSRA |= (1 << ADSC);
}

// Obter valor da FIFO
int ADC_Channel::get()
{
    return fifo.get();
}

// Retornar o número de valores disponíveis na FIFO
int ADC_Channel::available()
{
    return fifo.currentSize();
}

// Definição da interrupção do ADC
ISR(ADC_vect)
{
    // Identificar o canal atual
    int current_channel = ADMUX & 0x0F;

    // Obter a instância do canal
    ADC_Channel *adc = ADC_Channel::instance(current_channel);

    // Chamar o manipulador da instância
    if (adc != nullptr)
    {
        adc->adc_isr_handler();
    }
}
