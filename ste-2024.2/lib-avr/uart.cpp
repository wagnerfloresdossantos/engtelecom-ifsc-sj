#include "uart.h"
#include <avr/io.h>
#include <avr/interrupt.h>

UART* UART::instances[1];

UART::UART(unsigned long baudrate, Databits_t databits, Parity_t parity, Stopbits_t stopbits)
{
    instances[0] = this;
    // Setar baud-rate
    UCSR0A &= ~(1 << U2X0); // U2X0 = 0
    unsigned int ubrr = (Pcpu / 16) / baudrate -1;
    if (ubrr < 32)
    {
        UCSR0A |= (1 << U2X0);
        ubrr = (Pcpu / 8) / baudrate -1; 
    }
    UBRR0L = (unsigned char) (0xff & ubrr);
    UBRR0H = (unsigned char) (ubrr >> 8);

    // Configurar quadro
    UCSR0C = (parity << UPM00) | (stopbits << USBS0) | ((0x3 & databits) << UCSZ00);

    // Ligar Tx e Rx
    UCSR0B = (1 << TXEN0 | (1 << RXEN0) | (1 << RXCIE0));
    if((0x4 & databits) > 0)
        UCSR0B |= 1 << UCSZ02;
    else
        UCSR0B |= 0 << UCSZ02;
}

void UART::sync_put(char c)
{
    while( !(UCSR0A & (1 << UDRE0)) );
    UDR0 = c;
}

void UART::sync_puts(const char * s)
{
    while (*s)  // Enquanto não encontrar o caractere nulo '\0' indicando o fim da string
    {
        sync_put(*s);  // Enviar o caractere atual
        s++;      // Avançar para o próximo caractere
    }    
}

char UART::sync_get()
{
    while (!(UCSR0A & (1 << RXC0))); 
    return UDR0;
}


ISR(USART_UDRE_vect)
{
    UART * uart = UART::get_instance(0);
    uart->udre_isr_handler();
}

void UART::udre_isr_handler()
{
    if(tx_fifo.currentSize()>0)
        UDR0 = tx_fifo.get();
    else
        UCSR0B &= ~(1 << UDRIE0);
}   

// implementar o fifo_rx usando o USART_RX_vect

ISR(USART_RX_vect)
{
    UART * uart = UART::get_instance(0);
    uart->rx_isr_handler();
}

void UART::rx_isr_handler()
{
    if(!rx_fifo.isFull())
        rx_fifo.put(UDR0); // Armazenar dado recebido no FIFO

}


void UART::put(char c)
{
    tx_fifo.put(c);
    UCSR0B |=(1 << UDRIE0);

    /*
    Aula 02/12

    */
}

void UART::puts(const char * s)
{
    while (*s)  // Enquanto não encontrar o caractere nulo '\0' indicando o fim da string
    {
        put(*s);  // Enviar o caractere atual
        s++;      // Avançar para o próximo caractere
    }    
}

char UART::get()
{
    /*
    while (!(UCSR0A & (1 << RXC0))); 
    return UDR0;
    */
    while (rx_fifo.isEmpty()); // Esperar até que haja dados disponíveis
    return rx_fifo.get();      // Retornar dado do FIFO
    /*
    Aula de 02/12
    cli();
    char tmp = rx_fifo.get();
    sei();
    return tmp;
    */

}
/*
Aula 02/12
int UART::available()
{
    cli();
    int tmp = rx_fifo.size();
    sei();
    return tmp;
}
*/