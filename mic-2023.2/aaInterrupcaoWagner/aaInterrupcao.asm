;DEFINIÇÕES
.equ ON = PD2
.equ OFF = PD3    
.equ L0 = PB0        
.equ L1 = PB1
.def AUX = R16 
  
.ORG 0x0000        ; Reset vector
  RJMP setup       

.ORG 0x0002        ; Vetor (endereço na Flash) da INT0
  RJMP isr_int0     
  
.ORG 0x0004        ; Vetor (endereço na Flash) da INT1
  RJMP isr_int1     
  
.ORG 0x0034        ; primeira end. livre depois dos vetores
  
setup:
  ldi AUX,0x03     ; 0b00000011   
  
  out DDRB,AUX     ; configura PB3/2 como saída
  out PORTB,AUX    ; desliga os LEDs
  
  cbi DDRD, ON     ; configura o PD2 como entrada
  sbi PORTD, ON    ; liga o pull-up do PD2
  
  cbi DDRD, OFF    ; configura o PD3 como entrada
  sbi PORTD, OFF   ; liga o pull-up do PD3

  ldi AUX, 0b0000_1010    ; borda de descida em int0  e int1 gerar interrupção
  sts EICRA, AUX	  ; config. INT0 e INT1 sensível a borda
  sbi EIMSK, INT0         ; habilita a INT0
  sbi EIMSK, INT1         ; habilita a INT1
  
  sei              ; habilita a interrupção global ... 
                   ; ... (bit I do SREG)
main:
  sbi  PORTB,L0    ; desliga L0
  ldi r19, 160 
  rcall delay      ; delay 2s
  cbi  PORTB,L0    ; liga L0
  ldi r19, 160 
  rcall delay      ; delay 2s
  rjmp main

;-------------------------------------------------
; Rotina de Interrupção (ISR) da INT0 - ON - LIGAR
;-------------------------------------------------
isr_int0:
  push R16	  ; Salva o contexto (SREG)
  in R16, SREG
  push R16
  
  cbi  PORTB,L1   ; liga L1

  pop R16	  ; Restaura o contexto (SREG)
  out SREG,R16
  pop R16
  
  reti            ; retorna da interrupcao


;-------------------------------------------------
; Rotina de Interrupção (ISR) da INT1 - OFF - DESLIGA
;-------------------------------------------------
isr_int1:
  push R16	  ; Salva o contexto (SREG)
  in R16, SREG
  push R16
  
  sbi  PORTB,L1   ; desliga L1

fim:
  pop R16         ; Restaura o contexto (SREG)
  out SREG,R16
  pop R16
  
  reti            ; retorna da interrupcao
  
   
;------------------------------------------------------------
;SUB-ROTINA DE ATRASO Programável
;Depende do valor de R19 carregado antes da chamada.
;Exemplos: 
; - R19 = 16 --> 200ms 
; - R19 = 80 --> 1s 
;------------------------------------------------------------
delay:           
  push r17	 ; Salva os valores de r17,
  push r18	 ; ... r18,
  in r17,SREG    ; ...
  push r17       ; ... e SREG na pilha.

  ; Executa sub-rotina :
  clr r17
  clr r18
loop:            
  dec  R17       ;decrementa R17, começa com 0x00
  brne loop      ;enquanto R17 > 0 fica decrementando R17
  dec  R18       ;decrementa R18, começa com 0x00
  brne loop      ;enquanto R18 > 0 volta decrementar R18
  dec  R19       ;decrementa R19
  brne loop      ;enquanto R19 > 0 vai para volta

  pop r17         
  out SREG, r17  ; Restaura os valores de SREG,
  pop r18        ; ... r18
  pop r17        ; ... r17 da pilha

  ret
  


