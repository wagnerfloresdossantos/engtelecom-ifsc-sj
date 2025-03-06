### Alunos:
Gustavo Paulo 
https://github.com/gugasth

Deivid Fortunato Frederico
https://github.com/deividffrederico

Wagner Flores dos Santos
https://github.com/wagnerfloresdossantos

# Protocolo de Enlace para Comunicação Ponto a Ponto
Este projeto implementa um protocolo de enlace para comunicação ponto a ponto, projetado para operar em um canal sem fio de baixa taxa de dados. O protocolo é capaz de encapsular mensagens, detectar erros, garantir a entrega de quadros e gerenciar a sessão de comunicação entre dois dispositivos.

O sistema utiliza o serialEmu, um emulador de link serial, para simular a comunicação entre dois terminais. Isso facilita o desenvolvimento e teste do protocolo, abstraindo as particularidades de hardware.

## Funcionamento do Protocolo
O protocolo é baseado em uma arquitetura em camadas, onde cada camada é responsável por uma funcionalidade específica. As principais camadas são:

### Camada de Aplicação:
Responsável por enviar e receber dados da aplicação (por exemplo, mensagens de texto).
Converte os dados em quadros para serem enviados pela camada inferior.
### Camada ARQ (Automatic Repeat reQuest):
Implementa o mecanismo de garantia de entrega usando o protocolo Stop-and-Wait.
Utiliza uma fila de quadros para gerenciar os quadros a serem enviados.
Alterna entre os estados OCIOSO e ESPERA para enviar quadros e aguardar confirmações (ACKs).
Retransmite quadros em caso de timeout ou perda de ACK.
### Camada de Enquadramento:
Responsável por encapsular os quadros em um formato específico, adicionando delimitadores de início e fim (0x7e).
Realiza o byte stuffing para evitar conflitos com os delimitadores e bytes especiais.
Calcula e verifica o CRC-16-CCITT para detecção de erros.
### Camada Física:
Responsável pela transmissão e recepção dos quadros pela interface serial.
Utiliza o serialEmu para emular a comunicação serial entre dois terminais.

## Tutorial

###  Baixar o projeto
```
git clone endereço.git
```
```
git checkout enquadramento
```
### Utilizando venv (recomendado, mas opcional)
### Criar a venv (somente uma vez)
```
python3 -m venv venv
```
### entrar na venv
```
source venv/bin/activate
```
### baixar as dependências (somente uma vez)
```
pip install -r requirements.txt
```
### caso queira sair da venv
```
deactivate
```

## Exemplo de Fluxo:
### Envio de dados:
A aplicação envia uma mensagem (por exemplo, "Olá Mundo!").
A camada ARQ encapsula a mensagem em um quadro do tipo DATA e o enfileira.
Se o ARQ estiver no estado OCIOSO, o quadro é enviado imediatamente para a camada de enquadramento.
A camada de enquadramento adiciona delimitadores, realiza o byte stuffing e calcula o CRC.
O quadro é transmitido pela interface serial virtual criada pelo serialEmu.
### Recepção de Dados:
O quadro é recebido pela interface serial virtual no outro terminal.
A camada de enquadramento remove os delimitadores, realiza o byte unstuffing e verifica o CRC.
Se o CRC for válido, o quadro é passado para a camada ARQ.
A camada ARQ verifica o número de sequência e envia um ACK de confirmação.
O quadro é entregue à aplicação, que exibe a mensagem recebida.
### Confirmação (ACK):
O ACK é enviado de volta ao transmissor para confirmar o recebimento do quadro.
O transmissor alterna o número de sequência e envia o próximo quadro da fila, se houver.
### Retransmissão:
Se o transmissor não receber um ACK dentro do tempo limite (timeout), ele retransmite o último quadro enviado.


## Arquitetura do Projeto
O projeto é organizado em módulos, cada um responsável por uma camada do protocolo:

quadro.py: Define a classe Quadro, que representa um quadro no protocolo.

enquadramento.py: Implementa a camada de enquadramento, responsável por encapsular e desencapsular quadros.

arq.py: Implementa a camada ARQ, responsável pela garantia de entrega e controle de fluxo, utilizando uma fila de quadros.

aplicacao.py: Implementa a camada de aplicação, que interage com o usuário e envia/recebe dados.

subcamada.py: Define a classe base Subcamada, que serve como interface para as camadas do protocolo.

## 1.  Configuração dos Terminais
### Terminal 1
```
./serialemu -B 9600
```
```
/dev/pts/3 /dev/pts/4
```
```
python3 main.py /dev/pts/3
```
```
Olá Mundo!
```
```
Olá Mundo!
[Aplicação]: Olá Mundo!
[ARQ] Enfileirando quadro: Quadro(controle={'tipo': 'DATA', 'numero_sequencia': 0}, reservado=None, proto=text, dados=b'Ol\xc3\xa1 Mundo!', fcs=None)
[Enquadramento] Enviando quadro DATA: 7e0000744f6cc3a1204d756e646f218ed87e

[Enquadramento] CRC válido! Dados enviados para Aplicacao.
[ARQ] Recebido ACK: Quadro(controle={'tipo': 'ACK', 'numero_sequencia': 0}, reservado=None, proto=None, dados=None, fcs=bytearray(b'\x8b\x83'))
```
### Terminal 2
```
python3 main.py /dev/pts/4
```
```
[Enquadramento] CRC válido! Dados enviados para Aplicacao.
[ARQ] Recebido quadro DATA: Quadro(controle={'tipo': 'DATA', 'numero_sequencia': 0}, reservado=None, proto=None, dados=bytearray(b'tOl\xc3\xa1 Mundo!'), fcs=bytearray(b'\x8e\xd8'))
DATA Recebida: Olá Mundo!
[Enquadramento] Enviando quadro ACK: 7e80008b837e
```

### Para utlizar a ferramenta proto
Entre na pasta \proto_com_erros
```
./proto --serialPath /dev/pts/4 --debug --noSession
```

### UML do projeto 
![UML](/images/uml.png)

### UML do projeto com ARQ 
![UML](/images/modelagemArq.png)

### UML da MEF
![UML](/images/mefARQ.png)

### UML da MEF (com Fila)
![UML](/images/mefFilaArq.png)