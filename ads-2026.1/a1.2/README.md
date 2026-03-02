# A1.2 — Miniprojeto (ADS)  
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