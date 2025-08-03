# IFSC - Sistemas Embarcados - LibAVR

Nesta atividade construiremos uma biblioteca de funções de baixo-nível para uso na CPU AVR e na Placa Arduino. Usaremos as ferramentas do GCC e construiremos o sofware em C++.

Para construir a biblioteca os alunos devem seguir as orientações do professor, a serem registradas através do sistema acadêmico.

## Ao final, a biblioteca deverá incluir

* Uma HAL para os seguintes componentes de hardware: GPIO, UART, ADC, Timer, SPI;
* Um serviço de fila de funções para escanolamento de tarefas;
* Utilitários de Fifo e Lista lineares;
* Utilitário de gerenciamento de tempo (delay, etc).

## Dependências

Para satisfazer as dependências deste repositório, instalar os seguintes pacotes:
```bash
sudo apt-get install build-essential gcc-avr avr-libc avrdude
```

## Para gerar binários e programar a MCU

A biblioteca inclui um Makefile com as regras para geração do binário e programação do dispositivo. Algumas variáveis podem ser configuradas:

* APP := main.cpp => este é o programa principal, que será compilado, e deverá incluir a função main.
* COMPONENTS := gpio.o => esta é a lista de componentes a serem gerados. O arquivo objeto gpio.o do componente GPIO será gerado a partir do código-fonte em gpio.cpp. Ao incluir novos componentes (ex.: uart.cpp, adc.cpp), você deve atualizar esta lista para que o Makefile gere os componentes (ex.: COMPONENTS := gpio_pin.o uart.o adc.o).
* SERIAL_PORT := /dev/ttyACM0 => este é a porta serial á qual seu Arduino está conectado. Para verificar a porta correta, use o comando "ls /dev/tty*".
* CC_FLAGS => esta variável inclui as flags a serem passadas ao compilador. No Makefile há uma versão comentada desta variável que habilita o uso de floats no sprintf.

Para gerar o binário e programar o Arduino: make all

Para limpar o ambiente, excluindo os binários gerados: make clean
