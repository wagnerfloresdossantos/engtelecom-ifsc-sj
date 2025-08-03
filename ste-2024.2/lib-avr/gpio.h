#ifndef __GPIO_PIN_H__
#define __GPIO_PIN_H__

class GPIO_Pin {  
public:
   typedef void(*FuncPtr_t)(void);

private:
    static FuncPtr_t handlers[2];
    static const int PORT_ADDR[3];

    struct GPIO_Port
    {
        unsigned char pin;
        unsigned char ddr;
        unsigned char port;
    };
    GPIO_Port *port;
    unsigned char mask;

public:
    enum GPIO_Port_Name
    {
        GPIO_PortB = 0,
        GPIO_PortC = 1,
        GPIO_PortD = 2
    };

    enum GPIO_Direction
    {
        INPUT = 0,
        OUTPUT = 1,
        INT_LOW = 2,
        INT_CHANGE = 3,
        INT_FALLING = 4,
        INT_RISING = 5
    };

    enum GPIO_Level1
    {
        LOW = 0,
        HIGH = 1
    };

    GPIO_Pin(GPIO_Port_Name port_name,
            int pin,
            GPIO_Direction dir,
            FuncPtr_t handler = 0);
    void set();
    void clear();
    void write(int value);
    int read();
    static FuncPtr_t get_handler(int n){
        return handlers[n];
    };
};

#endif