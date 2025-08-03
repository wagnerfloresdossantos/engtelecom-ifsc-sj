#include "gpio.h"
#include <avr/io.h>
#include <avr/interrupt.h>

const int GPIO_Pin::PORT_ADDR[3] = {0X23,0x26,0x29};

GPIO_Pin::FuncPtr_t GPIO_Pin::handlers[2];

// INT0
ISR(INT0_vect){
    GPIO_Pin::FuncPtr_t handler_func = GPIO_Pin::get_handler(0);
    handler_func();

}

// INT1
ISR(INT1_vect){
    GPIO_Pin::FuncPtr_t handler_func = GPIO_Pin::get_handler(1);
    handler_func();
}

GPIO_Pin::GPIO_Pin(GPIO_Port_Name port_name,
                    int pin,
                    GPIO_Direction dir,
                    FuncPtr_t handler)
            
{
    if(dir >= INT_LOW)
    {
    int int_pin = pin -2;
    int int_sens = dir -2;
    handlers[int_pin] = handler;
    // configurar sensibilidade da interrupção
    unsigned char tmp = EICRA;
    tmp &= -(3 << int_pin*2);
    tmp = int_sens <<(int_pin*2);
    // ligar a interrupção
    EIMSK |= 1 << int_pin;
    }
    else
    {
    // pinmode
    mask = 1 << pin;
    port = (GPIO_Port*) PORT_ADDR[port_name];
    if (dir == OUTPUT)
        port->ddr |= mask;
    else
        port->ddr &= ~mask;
    }
}

void GPIO_Pin::set()
{
    // high
    port->port |= mask; 
}

void GPIO_Pin::clear()
{
    // low
    port->port &= ~mask; 
}

void GPIO_Pin::write(int value)
{
  
    if (value == HIGH) {
        set(); 
    } else {
        clear(); 
    }
 
}

int GPIO_Pin::read()
{
    return (port->pin & mask) ? HIGH : LOW;
}