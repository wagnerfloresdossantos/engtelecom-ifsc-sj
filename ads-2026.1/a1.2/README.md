# A1.2 — Miniprojeto (ADS)

**Medição ativa com `iperf` + medição passiva com `tcpdump/tshark` no IMUNES**  
Planejamento fatorial completo **2²** com **8 repetições** por tratamento, totalizando **32 execuções**.

Este repositório contém dois scripts principais:

- **`run_experimento.py`**: executa automaticamente os 32 testes no IMUNES, gera tráfego TCP e UDP conforme a topologia, captura tráfego no enlace entre roteadores e salva o **`resultados.csv`**.
- **`analisar_resultados.py`**: lê o CSV, calcula estatísticas (média, desvio padrão e IC 95%), estima efeitos do planejamento fatorial 2² e gera gráficos.

---

## Topologia utilizada

A topologia do experimento possui quatro PCs e dois roteadores:

- **Fluxo TCP principal:** `pc1 -> pc2`
- **Fluxo UDP de background:** `pc4 -> pc3`

### Endereços utilizados
- `pc1`: `10.0.0.20/24`
- `pc2`: `10.0.2.20/24`
- `pc3`: `10.0.3.20/24`
- `pc4`: `10.0.4.20/24`

### Enlace de interesse
O enlace entre `router1` e `router2` é o enlace central do experimento.  
Nele são aplicados:

- o **delay** do fator experimental
- a **captura com tcpdump**
- o compartilhamento entre o tráfego TCP e o tráfego UDP de background

---

## Passo a passo de execução

1. Abrir o **IMUNES** e carregar a topologia.
2. Clicar em **Run** no IMUNES.
3. No terminal do host, executar: `
python3 run_experimento.py
`

## O que o script faz automaticamente

Quando você executar:
`python3 run_experimento.py`

o script irá:

### Preparação do ambiente
* entrar no pc2
* matar um iperf TCP antigo, se existir
* subir o servidor TCP iperf no pc2
* validar se a porta 5001 está escutando
* entrar no pc3
* matar um iperf UDP antigo, se existir
* subir o servidor UDP iperf no pc3
* validar se a porta 5002 está escutando
* limpar qualquer delay antigo no router1

### Execução do experimento

Para cada cenário experimental o script irá:

* configurar Reno ou Cubic no pc1
* aplicar 10 ms ou 50 ms de delay no enlace entre roteadores
* iniciar tráfego UDP de background (pc4 → pc3)
* iniciar captura tcpdump no enlace entre roteadores
* rodar iperf TCP (pc1 → pc2)
* encerrar a captura
* copiar o arquivo .pcap
* calcular retransmissões via tshark
* gravar resultados no CSV

## Fatores e respostas
### Fatores (variáveis de entrada)
#### Fator A — Algoritmo TCP
* reno
* cubic

### Fator D — Delay no enlace entre roteadores
Aplicado via tc/netem:
* 10 ms
* 50 ms

## Variáveis de saída
### Vazão média TCP
`iperf_avg_mbps`

Obtida via iperf.

Representa a vazão média do fluxo TCP principal.

### Taxa de retransmissão
`retrans_rate

Calculada via tshark.

Fórmula:

`retrans_rate = n_retrans / n_dados`

onde:

`n_dados` = segmentos TCP com payload

`n_retrans = retransmissões detectadas

## Planejamento experimental

O experimento segue um planejamento fatorial 2².

### Combinações
Algoritmo	Delay
* Reno	10 ms
* Reno	50 ms
* Cubic	10 ms
* Cubic	50 ms

Cada combinação é executada 8 vezes.

Total de execuções:

`4 combinações × 8 repetições = 32 execuções`
## Saída gerada

Todos os resultados são armazenados em:

`resultados_imunes/`

Arquivo principal:

`resultados_imunes/resultados.csv`

Cada linha do CSV representa uma execução do experimento.

### Estrutura do CSV

Exemplo de colunas:

* timestamp
* rep
* alg
* delay_ms
* bg_udp_mbps
* iperf_avg_mbps
* tcp_payload_bytes
* n_dados
* n_retrans
* retrans_rate
* pcap_file

## Pré-requisitos
No host (Ubuntu)

#### Instalar ferramentas necessárias:

`sudo apt update`\
`sudo apt install python3 iperf tcpdump tshark`

Também é necessário ter:

*  `IMUNES` instalado
* topologia criada
* permissão sudo

Autor:\
Wagner Flores dos Santos\
Engenharia de Telecomunicações — IFSC São José