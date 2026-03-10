# A1.2 — Miniprojeto (ADS)  

## Passo a passo execução

1. abrir IMUNES e carregar a topologia
2. clicar em Run no IMUNES
3. no terminal do host:
`python3 run_experimento.py

## O que o script faz automaticamente

Quando você rodar:

`python3 experimento_imunes.py
 O que o script faz automaticamente

Quando você rodar:

python3 experimento_imunes.py

ele já vai:

- entrar no pc2

- matar um iperf antigo, se existir

- subir o iperf server no pc2

- validar se a porta 5001 está escutando

- limpar delay antigo no router1

- para cada cenário:

- configurar Reno ou Cubic no pc1

- aplicar 10 ms ou 50 ms no router1

- iniciar tcpdump no pc1

- rodar iperf client no pc1

- copiar o .pcap

- calcular retransmissões com tshark

- gravar no CSV


**Medição ativa com `iperf` + medição passiva com `tcpdump/tshark` no IMUNES**  
Planejamento fatorial completo **2²** com **8 repetições** por tratamento (total **32 execuções**).

Este repositório contém dois scripts principais:

- **`run_experimento.py`**: executa automaticamente os 32 testes no IMUNES, captura tráfego e salva **`resultados.csv`**.  
- **`analisar_resultados.py`**: lê o CSV, calcula estatísticas (média/DP/IC 95%), estima efeitos do 2² e gera gráficos.

---


## Fatores e respostas

### Fatores (entradas)
- **Fator A — Algoritmo TCP:** `reno` / `cubic`
- **Fator D — Delay (netem) no enlace entre roteadores:** `10 ms` / `50 ms`

### Variáveis de saída (respostas)
- **`iperf_avg_mbps`**: vazão média medida via `iperf` (Mbit/s)
- **`retrans_rate`**: taxa de retransmissão estimada via `tshark`
  - `retrans_rate = n_retrans / n_dados`

---

## Pré-requisitos

### No host (Ubuntu)
Instale ferramentas usadas pelo script:
- `python3` (e libs python)
- `iperf` (versão 2.x)
- `tcpdump`
- `tshark`
- `imunes` (topologia já criada)


Autor:\
Wagner Flores dos Santos\
Engenharia de Telecomunicações — IFSC São José