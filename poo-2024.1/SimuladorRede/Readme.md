# Projeto prático 02: Simulador de Rede

## Aluno: Wagner Flores dos Santos

### Instruções para criar uma nova regra de filtragem, um novo pacote IP e simular o processamento do pacote


### Criar regra de filtragem

Permite ao usuário criar uma nova regra de filtragem no firewall.
O usuário deve informar o endereço IP de origem, porta IP de origem, endereço IP de destino, porta IP de destino, e a ação (encaminhar ou descartar).

```
5. Criar regra de filtragem
```
O Usuário deve informar os seguintes dados:
```Digite o endereço IP de origem da regra: 
Digite a porta IP de origem da regra: 
2Digite o endereço IP de destino da regra: 
Digite a porta IP de destino da regra: 
Digite o endereço MAC de destino da regra: 
Digite o conteúdo da regra: 
Escolha a ação (1 - ENCAMINHAR, 2 - DESCARTAR): 
Regra adicionada com sucesso.
```

### Simular processamento de pacote e criação de pacote

```Java 
7. Simular processamento de pacote
```

O usuário deve informar os seguintes dados para criar um pacote IP:

```
Digite o endereço IP de origem: 
Digite a porta IP de origem: 
Digite o endereço IP de destino: 
Digite a porta IP de destino: 
Digite o endereço MAC de destino: 
Digite o conteúdo do pacote: 
```

A aplicação simula o processamento do pacote pelos dispositivos na rede e exibe o comportamento de cada dispositivo:


#### Comutador: Indica se o pacote foi encaminhado para a porta física correta ou para todas as portas.

Configuração Comutador
```
comutador.inserirEntradaTabelaMac("A2",1);
comutador.inserirEntradaTabelaMac("A3",2);
comutador.inserirEntradaTabelaMac("A4",3);
comutador.inserirEntradaTabelaMac("A5",4);
```
Saída esperada se o MAC informado está na tabela (MAC de destino: A2):

```
Comutador: Pacote encaminhado para a porta: 1
```
senão:
```
Comutador: Endereço MAC desconhecido. Pacote encaminhado para todas as portas, exceto a porta de origem.
Comutador: Pacote encaminhado para a porta: 1
Comutador: Pacote encaminhado para a porta: 2
Comutador: Pacote encaminhado para a porta: 3
Comutador: Pacote encaminhado para a porta: 4
```

#### Roteador: Indica se o pacote foi encaminhado para uma rede local ou para a Internet "eth0" (onde encontra-se o firewall).

Configuração da rede
```
this.roteador = new Roteador("B2", "2001", new HashMap<>(), "eth0");  // HashMap para tabela de rotas
```
```
roteador.addRota("1xxx", "eth1"); // Rota para a rede 1xxx
roteador.addRota("2xxx", "eth2"); // Rota para a rede 2xxx
```
Saída esperada se existir rota (IP: 2005):

```
Roteador: Pacote encaminhado para a rede: 2xxx na porta: eth2
```
Senão:
```
Roteador: Rede desconhecida. Pacote encaminhado para a porta de saída padrão: eth0
```
#### Firewall: Indica se o pacote foi encaminhado ou descartado, e exibe o índice da regra de filtragem que foi satisfeita.

Regras ao firewall:
```
firewall.addRegra(new RegrasFiltragem("1001", "8080", "2002", "80", "A2", "Olá, mundo!", Acao.ENCAMINHAR));
firewall.addRegra(new RegrasFiltragem("2001", "22", "3001", "443", "B3", "Teste de segurança", Acao.DESCARTAR));
```
Saída esperada se existir Regra:
```
Firewall: Pacote encaminhado conforme a regra 0: ENCAMINHAR
```

Senão:
```
Firewall: Nenhuma regra satisfeita. Pacote descartado.
```

### Indicar quais funcionalidades foram implementadas e quais não foram

Acredito que todas as fuincionabilidades foram criadas.