.INCLUDE <m328Pdef.inc>
    
.equ LED = PD0  ;LED é o substituto de PD0 na programacao
.equ LED2 = PD1 ;LED2 é o substituto de PD1 na programacao
.equ LED3 = PD2 ;LED3 é o substituto de PD2 na programacao
.equ LED4 = PD3 ;LED4 é o substituto de PD3 na programacao
.equ LED5 = PD4 ;LED5 é o substituto de PD4 na programacao
.equ LED6 = PD5 ;LED6 é o substituto de PD5 na programacao
.equ LED7 = PD6 ;LED7 é o substituto de PD6 na programacao
.equ LED8 = PD7 ;LED8 é o substituto de PD7 na programacao
    
.equ BOTAO = PB0 ;botão ajuste é o substituto de PB0 na programacao
.equ BOTAO2 = PB1;botão seleção é o substituto de PB1 na programacao
    
.def AUX = R16 ;R16 tem agora o nome de AUX

setup:
 LDI AUX,0b11111111 ;carrega AUX com o valor 0b11111111
    
    OUT DDRD, AUX ;configura todos os pinos do DDRD como saida
    OUT DDRB, AUX ;configura todos os pinos do DDRB como saida
    
    OUT PORTD, AUX ;configura todos os pinos do PORTD como pull-up
    OUT PORTB, AUX ;configura todos os pinos do PORTD como pull-up
 
main: 
    rcall ligaTodosLEDs

pressAjuste:
    sbic PINB,BOTAO ;verifica se o botão ajuste foi pressionado, se sim salta uma linha
    rjmp naoPressAjuste ; salta para rotulo  
    rcall desligaLEDsMenos ;chama subrotina 
    
pressSelec:
    sbic PINB,BOTAO2 ;;verifica se o botão select foi pressionado, se sim salta uma linha
    rjmp naoPressSelec ; salta para rotulo
    rcall desligaLEDsMais ;chama subrotina
    rjmp pressAjuste ; salta para rotulo
    
naoPressAjuste:
    rcall ligaLEDsMenos ;chama subrotina     
    rjmp pressSelec ; salta para rotulo
    
naoPressSelec:
    rcall ligaLEDsMais  ;chama subrotina
    rjmp PressAjuste ; salta para rotulo
     
;--------------------------------------
; SUBROTINA LIGA TODOS LEDS
;--------------------------------------
ligaTodosLEDs:	
    ; Liga todos os LED's
    cbi PORTD,LED 
    cbi PORTD,LED2
    cbi PORTD,LED3
    cbi PORTD,LED4
    cbi PORTD,LED5
    cbi PORTD,LED6
    cbi PORTD,LED7
    cbi PORTD,LED8
    
    ret
    
;--------------------------------------
; SUBROTINA DESLIGA LEDS MENOS SIGNIFICATIVOS
;--------------------------------------
desligaLEDsMenos:	
    ; desliiga os LED's menos significativios  
    sbi PORTD,LED 
    sbi PORTD,LED2
    sbi PORTD,LED3
    sbi PORTD,LED4
    
    ret
    
;--------------------------------------
; SUBROTINA DESLIGA LEDS MENOS SIGNIFICATIVOS
;--------------------------------------
desligaLEDsMais:	
    ; desliiga os LED's mais significativios  
    sbi PORTD,LED5 
    sbi PORTD,LED6
    sbi PORTD,LED7
    sbi PORTD,LED8
    
    ret
    
    
;--------------------------------------
; SUBROTINA LIGA LEDS MENOS SIGNIFICATIVOS
;--------------------------------------
ligaLEDsMenos:	
    ; liga os LED's menos significativios  
    cbi PORTD,LED 
    cbi PORTD,LED2
    cbi PORTD,LED3
    cbi PORTD,LED4
    
    ret
    
;--------------------------------------
; SUBROTINA LIGA LEDS MAIS SIGNIFICATIVOS
;--------------------------------------
ligaLEDsMais:	
    ; liga os LED's menos significativios  
    cbi PORTD,LED5 
    cbi PORTD,LED6
    cbi PORTD,LED7
    cbi PORTD,LED8
    
    ret
    