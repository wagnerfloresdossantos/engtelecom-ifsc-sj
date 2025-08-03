#ifndef __UART_H__
#define __UART_H__

#include "avr/io.h"
#include "fifo.h"

class UART
{
private:
    Fifo<16, char> tx_fifo;
    Fifo<16, char> rx_fifo;

    static UART* instances[1];  // Altere o número de instâncias se necessário

public:
    static const unsigned long Pcpu = 16e6;

    enum Databits_t
    {
        DATABITS_5 = 0,
        DATABITS_6 = 1,
        DATABITS_7 = 2,
        DATABITS_8 = 3,
        DATABITS_9 = 7
    };

    enum Parity_t
    {
        PARITY_NONE = 0,
        PARITY_EVEN = 2,
        PARITY_ODD = 3
    };

    enum Stopbits_t
    {
        STOPBITS_1 = 0,
        STOPBITS_2 = 1
    };
    
    UART(unsigned long baudrate = 9600, 
          Databits_t databits = DATABITS_8, 
          Parity_t parity = PARITY_NONE, 
          Stopbits_t stopbits = STOPBITS_1);

    void sync_put(char c);
    void sync_puts(const char *s);
    char sync_get();
    
    void put(char c);
    void puts(const char *s);
    char get();

    void udre_isr_handler();            
    void rx_isr_handler();              

    static UART * get_instance(int n)
    {
        return instances[n];
    }
};

#endif
