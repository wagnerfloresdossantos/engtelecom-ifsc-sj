#include "gpio.h"
#include "uart.h"
#include <avr/interrupt.h>
#include <stdio.h>

// GPIO e UART
GPIO_Pin led1(GPIO_Pin::GPIO_PortB, 5, GPIO_Pin::OUTPUT);
UART Serial(19200, UART::DATABITS_8, UART::PARITY_NONE, UART::STOPBITS_1);

// ADC
//ADC_Channel adc0(ADC_Channel::ADC_Channel_0);
//ADC_Channel adc1(ADC_Channel::ADC_Channel_1); 

// Botão com interrupção
void btn_handler()
{
    static bool led_state = 0;
    led_state = !led_state;
    led1.write(led_state ? GPIO_Pin::HIGH : GPIO_Pin::LOW);
    Serial.sync_put('b');
}

GPIO_Pin btn(GPIO_Pin::GPIO_PortD, 3, GPIO_Pin::INT_RISING, btn_handler);

// Delay de software
void soft_delay()
{
    unsigned long long x = 0xffff;
    while (x--) {}
}

void setup()
{
    sei();
    Serial.sync_puts("Setup completo\n");
}

void loop()
{
    // Leituras ADC
    int adc0_val = 0, adc1_val = 0;

    adc0.start();
    while (adc0.available() < 8);
    for (int i = 0; i < 8; i++) adc0_val += adc0.get();
    adc0_val /= 8;

    adc1.start();
    while (adc1.available() < 8);
    for (int i = 0; i < 8; i++) adc1_val += adc1.get();
    adc1_val /= 8;

    // Envia resultados via UART
    char str[64];
    sprintf(str, "ADC0: %d\nADC1: %d\n", adc0_val, adc1_val);
    Serial.puts(str);

    soft_delay();
}

int main()
{
    setup();
    while (true) loop();
}
