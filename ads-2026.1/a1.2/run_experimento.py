#!/usr/bin/env python3
"""
Automação do experimento (planejamento fatorial 2^2) no IMUNES.

Fatores:
  A: algoritmo TCP (reno / cubic) aplicado no pc1
  D: delay (10 / 50 ms) aplicado no enlace entre roteadores (router1, iface eth1)

Medições:
  - vazão média via iperf (medição ativa)
  - taxa de retransmissão via tcpdump + tshark (medição passiva)

Saída:
  - resultados_imunes/resultados.csv (1 linha por execução)
  - PCAPs são gerados em /tmp dentro do nó e copiados temporariamente ao host
"""

import csv
import re
import subprocess
from datetime import datetime
from pathlib import Path

# =========================
# CENÁRIO / PARÂMETROS FIXOS
# =========================

# Nomes dos nós no IMUNES
PC1 = "pc1"   # cliente (onde rodam iperf client e tcpdump)
PC2 = "pc2"   # servidor (onde roda iperf server)

# IPs usados na topologia (importante para filtros do tcpdump/tshark)
PC1_IP = "10.0.0.20"
PC2_IP = "10.0.2.20"

# Delay é aplicado no enlace entre roteadores (fator D)
ROUTER_DELAY_NODE = "router1"
ROUTER_DELAY_IFACE = "eth1"   # interface do roteador no enlace com delay (ex.: 10.0.1.1/24)

# Duração padrão do iperf (tempo de cada execução)
DURACAO_IPERF_S = 30

# Níveis do planejamento fatorial
ALGS = ["reno", "cubic"]      # fator A
DELAYS_MS = [10, 50]          # fator D
REPS = 8                      # repetições por tratamento (total esperado = 2*2*8 = 32)

# Diretório de saída (no host)
OUTDIR = Path("resultados_imunes")
OUTDIR.mkdir(exist_ok=True)
CSV_PATH = OUTDIR / "resultados.csv"


# =========================
# FUNÇÕES AUXILIARES DE EXECUÇÃO
# =========================

def sh(cmd: str, check=True) -> str:
    """
    Executa um comando no HOST (máquina real) e devolve stdout+stderr.

    - check=True: se o comando falhar, levanta RuntimeError e interrompe o script.
    - Importante para debugar: imprime o comando antes de rodar.
    """
    print(f"$ {cmd}")
    p = subprocess.run(
        cmd,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    if check and p.returncode != 0:
        raise RuntimeError(f"Falhou ({p.returncode}): {cmd}\n---\n{p.stdout}\n---")
    return p.stdout


def himage(node: str, cmd: str) -> str:
    """
    Executa um comando *dentro de um nó do IMUNES* via 'himage'.

    Observação:
    - aqui assumimos o padrão: sudo himage <node> <cmd>
    - o cmd normalmente é algo tipo: sh -lc '...'
    """
    return sh(f"sudo himage {node} {cmd}")


def hcp(src: str, dst: str) -> None:
    """
    Copia arquivos entre host <-> nós do IMUNES via 'hcp'.
    Exemplo de src: "pc1:/tmp/arquivo.pcap"
    """
    sh(f"sudo hcp {src} {dst}", check=True)


# =========================
# PREPARAÇÃO DO SERVIDOR IPERF
# =========================

def ensure_iperf_server():
    """
    Garante que o iperf server está rodando no pc2:5001.

    Por que isso existe?
    - Se o servidor não estiver ativo, o iperf client falha e perde a execução.
    - O script "mata e sobe" o servidor para começar cada bateria em um estado conhecido.

    Como valida?
    - Confere PID (kill -0)
    - Confere porta 5001 escutando (ss -lnt)
    """
    # 1) Mata um server antigo (se existir) e limpa pid/log anteriores.
    himage(PC2, r"""sh -lc '
        pid=$(cat /tmp/iperf.pid 2>/dev/null || true)
        case "$pid" in
            (""|*[!0-9]*) true ;;
            (*) kill -9 "$pid" 2>/dev/null || true ;;
        esac
        rm -f /tmp/iperf.pid /tmp/iperf.log
    '""")

    # 2) Sobe server em background usando nohup.
    # Obs.: sem nohup + </dev/null o iperf pode ficar “preso” ao terminal.
    himage(PC2, r"""sh -lc '
        nohup iperf -s >/tmp/iperf.log 2>&1 </dev/null &
        echo $! > /tmp/iperf.pid
        sleep 0.2
    '""")

    # 3) Validação: PID existe, processo está vivo e porta 5001 está aberta.
    out = himage(PC2, r"""sh -lc '
        pid=$(cat /tmp/iperf.pid 2>/dev/null || true)
        echo "PID=[$pid]"
        case "$pid" in (""|*[!0-9]*) echo "PID inválido"; cat /tmp/iperf.log 2>/dev/null; exit 1 ;; esac

        kill -0 "$pid" 2>/dev/null || { echo "iperf morreu"; cat /tmp/iperf.log 2>/dev/null; exit 1; }

        for i in $(seq 1 30); do
            ss -lnt 2>/dev/null | grep -q ":5001" && echo OK && exit 0
            sleep 0.1
        done

        echo FAIL
        ss -lntp 2>/dev/null | head -n 50 || true
        echo "LOG:"
        cat /tmp/iperf.log 2>/dev/null || true
        exit 1
    '""")

    if "OK" not in out:
        raise RuntimeError("iperf server NÃO está escutando no pc2:5001 (mesmo após tentativa de start).")


# =========================
# CONFIGURAÇÃO DOS FATORES (A e D)
# =========================

def detect_pc1_iface_to_pc2() -> str:
    """
    Descobre automaticamente qual interface do pc1 é usada para alcançar o pc2.

    Por que isso é importante?
    - No IMUNES, o nome da interface pode variar (eth0/eth1/...) dependendo do cenário.
    - Se capturar na interface errada, o tcpdump pega 0 pacotes e a métrica fica inválida.

    Como funciona?
    - 'ip route get <ip>' retorna a rota e informa 'dev <iface>'.
    """
    out = himage(PC1, f"sh -lc 'ip route get {PC2_IP} | head -n1'")
    m = re.search(r"dev\s+(\S+)", out)
    if not m:
        raise RuntimeError(f"Não consegui detectar interface do pc1. Saída:\n{out}")
    return m.group(1)


def set_tcp_cc(alg: str):
    """
    Configura o algoritmo de controle de congestionamento TCP (fator A) no pc1.
    Ex.: reno ou cubic.
    """
    himage(PC1, f"sh -lc 'sysctl -w net.ipv4.tcp_congestion_control={alg}'")


def clear_delay():
    """
    Remove qualquer qdisc netem anterior na interface do roteador.

    Motivo:
    - Evita que um delay “antigo” fique acumulado se o script foi interrompido antes.
    """
    himage(ROUTER_DELAY_NODE, f"sh -lc 'tc qdisc del dev {ROUTER_DELAY_IFACE} root 2>/dev/null || true'")


def set_delay_ms(delay_ms: int):
    """
    Aplica o delay (fator D) no enlace entre roteadores usando tc/netem.

    Implementação:
    - tenta 'add' (primeira vez)
    - se já existir, faz 'change'
    """
    add_cmd = f"tc qdisc add dev {ROUTER_DELAY_IFACE} root netem delay {delay_ms}ms"
    chg_cmd = f"tc qdisc change dev {ROUTER_DELAY_IFACE} root netem delay {delay_ms}ms"
    out = himage(ROUTER_DELAY_NODE, f"sh -lc '{add_cmd} || {chg_cmd}'")
    return out


# =========================
# EXTRAÇÃO DE MÉTRICAS
# =========================

def parse_iperf_mbps(iperf_out: str) -> float:
    """
    Extrai a taxa final do iperf em Mbit/s.

    Observação:
    - iperf pode mostrar Mbits/sec ou Gbits/sec.
    - aqui convertemos Gbits/sec -> Mbits/sec (x1000).
    """
    lines = [l.strip() for l in iperf_out.splitlines() if "Mbits/sec" in l or "Gbits/sec" in l]
    if not lines:
        raise RuntimeError(f"Não achei taxa no iperf:\n{iperf_out}")

    last = lines[-1].split()
    for i, tok in enumerate(last):
        if tok in ("Mbits/sec", "Gbits/sec") and i > 0:
            val = float(last[i - 1])
            if tok == "Gbits/sec":
                val *= 1000.0
            return val
    raise RuntimeError(f"Não consegui extrair Mbps da linha:\n{lines[-1]}")


def tshark_count(pcap_path: Path, display_filter: str) -> int:
    """
    Conta pacotes/linhas que casam com um display filter do tshark.

    Detalhe:
    - '-n' desativa resolução DNS (mais rápido e evita variações).
    - wc -l conta o número de linhas retornadas.
    """
    cmd = f'tshark -n -r "{pcap_path}" -Y "{display_filter}" 2>/dev/null | wc -l'
    out = sh(cmd)
    return int(out.strip())


def himage_nc(node: str, cmd: str) -> str:
    """
    Variante do himage que NÃO falha o script se o comando der erro.
    Útil para operações de limpeza (kill de processos que podem não existir, rm, etc.).
    """
    return sh(f"sudo himage {node} {cmd}", check=False)


# =========================
# EXECUÇÃO DE UMA REPETIÇÃO (1 run)
# =========================

def run_one(alg: str, delay_ms: int, rep: int) -> dict:
    """
    Executa uma repetição do experimento (um tratamento específico).

    Passos (resumo):
      1) aplica delay e algoritmo
      2) inicia captura tcpdump (pc1)
      3) roda iperf client (pc1 -> pc2)
      4) encerra tcpdump de forma controlada (SIGINT)
      5) copia PCAP para o host e calcula métricas via tshark
      6) devolve um dicionário para escrever no CSV
    """
    ts = datetime.now().isoformat(timespec="seconds")

    # Descobre a interface correta para capturar o fluxo até o pc2
    iface_pc1 = detect_pc1_iface_to_pc2()

    # Nome do PCAP para organização
    pcap_name = f"{alg}_{delay_ms}ms_rep{rep}.pcap"
    pcap_node = f"/tmp/{pcap_name}"
    pcap_host = OUTDIR / pcap_name

    # 1) Aplica fatores (ordem não muda o resultado, mas mantém padrão)
    set_delay_ms(delay_ms)
    set_tcp_cc(alg)

    # 2) Limpeza: garante que não existe tcpdump antigo rodando e remove arquivos do run anterior
    himage_nc(
        PC1,
        f"sh -lc '"
        f"pid=$(cat /tmp/tcpdump.pid 2>/dev/null || true); "
        f"case \"$pid\" in (\"\"|*[!0-9]*) true ;; (*) kill -9 \"$pid\" 2>/dev/null || true ;; esac; "
        f"rm -f /tmp/tcpdump.pid /tmp/tcpdump.log {pcap_node} 2>/dev/null || true"
        f"'"
    )

    # 3) Start tcpdump em background
    #    - captura apenas o fluxo do iperf (host pc2 e porta 5001)
    #    - '-U' tenta “flush” mais frequente (reduz chance de PCAP incompleto)
    start_cmd = (
        f"rm -f {pcap_node} /tmp/tcpdump.pid /tmp/tcpdump.log; "
        f"nohup tcpdump -U -Z root -s 128 -i {iface_pc1} -w {pcap_node} "
        f"'tcp and host {PC2_IP} and port 5001' "
        f">/tmp/tcpdump.log 2>&1 </dev/null & "
        f"sleep 0.2; "
        f"pgrep -f \"tcpdump.*-w {pcap_node}\" | tail -n 1 > /tmp/tcpdump.pid; "
        f"pid=$(cat /tmp/tcpdump.pid 2>/dev/null); "
        f"case \"$pid\" in (\"\"|*[!0-9]*) echo FAIL; echo PID=[$pid]; cat /tmp/tcpdump.log; exit 1 ;; esac; "
        f"kill -0 \"$pid\" 2>/dev/null && echo OK || "
        f"(echo FAIL; echo PID=[$pid]; cat /tmp/tcpdump.log; exit 1)"
    )
    himage(PC1, f"sh -lc \"{start_cmd}\"")

    # 4) Executa iperf client
    # check=False porque em alguns cenários um retorno 130 pode ocorrer (sinal/terminal),
    # mas ainda assim o output pode conter a taxa final.
    iperf_out = sh(
        f"sudo himage {PC1} sh -lc 'iperf -c {PC2_IP} -t {DURACAO_IPERF_S}'",
        check=False
    )
    mbps = parse_iperf_mbps(iperf_out)

    # 5) Encerra tcpdump “bonito” (SIGINT) e espera o arquivo estabilizar
    # (isso evita PCAP truncado/corrompido).
    himage(PC1, f"""sh -lc '
        pid=$(cat /tmp/tcpdump.pid 2>/dev/null || true)
        case "$pid" in (""|*[!0-9]*) exit 0 ;; esac

        kill -INT "$pid" 2>/dev/null || true

        for i in $(seq 1 50); do
          kill -0 "$pid" 2>/dev/null || break
          sleep 0.1
        done

        kill -0 "$pid" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true

        last=-1
        for i in $(seq 1 30); do
          sz=$(stat -c %s "{pcap_node}" 2>/dev/null || echo 0)
          [ "$sz" -eq "$last" ] && break
          last="$sz"
          sleep 0.1
        done
    '""")

    # 6) Valida se PCAP tem conteúdo (se ficar vazio, algo falhou: interface, filtro, iperf, etc.)
    himage(
        PC1,
        f"sh -lc 'test -s {pcap_node} || "
        f"(echo \"PCAP vazio\"; ls -l {pcap_node} 2>/dev/null; cat /tmp/tcpdump.log; exit 1)'"
    )

    # 7) Copia PCAP para o host (para processar com tshark no host)
    hcp(f"{PC1}:{pcap_node}", str(pcap_host))

    # 8) Métricas via tshark
    # total: segmentos TCP com payload (tcp.len>0) enviados do pc1 para porta 5001 (iperf)
    total = tshark_count(pcap_host, f"ip.src=={PC1_IP} and tcp.len>0 and tcp.dstport==5001")

    # retrans: conta retransmissões detectadas pelo analisador do Wireshark
    retrans = tshark_count(
        pcap_host,
        f"ip.src=={PC1_IP} and tcp.len>0 and tcp.dstport==5001 and "
        f"(tcp.analysis.retransmission or tcp.analysis.fast_retransmission)"
    )

    # taxa de retransmissão (evita divisão por zero se algo muito estranho acontecer)
    retrans_rate = (retrans / total) if total > 0 else 0.0

    # Limpa PCAP do host para não acumular arquivos gigantes (o CSV é o que importa)
    pcap_host.unlink(missing_ok=True)

    # Linha final a ser escrita no CSV
    return {
        "timestamp": ts,
        "rep": rep,
        "alg": alg,
        "delay_ms": delay_ms,
        "iperf_avg_mbps": mbps,
        "n_dados": total,
        "n_retrans": retrans,
        "retrans_rate": retrans_rate,
        "pcap_file": pcap_name,
    }


# =========================
# LOOP DO PLANEJAMENTO (32 execuções)
# =========================

def main():
    # 1) Garante que o servidor iperf está rodando antes de começar a bateria
    ensure_iperf_server()

    # 2) Remove delay residual (boa prática quando o script foi interrompido antes)
    clear_delay()

    # Se CSV não existe, cria cabeçalho; se existe, apenas adiciona linhas
    write_header = not CSV_PATH.exists()
    with open(CSV_PATH, "a", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "timestamp", "rep", "alg", "delay_ms",
                "iperf_avg_mbps", "n_dados", "n_retrans", "retrans_rate", "pcap_file"
            ]
        )
        if write_header:
            w.writeheader()

        # Ordem dos loops define a ordem das linhas no CSV (facilita conferência)
        for alg in ALGS:
            for delay in DELAYS_MS:
                for rep in range(1, REPS + 1):
                    print(f"\n=== RUN alg={alg} delay={delay}ms rep={rep} ===")
                    row = run_one(alg, delay, rep)
                    w.writerow(row)
                    f.flush()  # garante que grava mesmo se der erro no meio

    print(f"\nOK! CSV: {CSV_PATH}")
    print(f"PCAPs temporários (gerados durante as execuções) ficam em: {OUTDIR}/")
    print("\nPara limpar o delay ao final:")
    print(f"  sudo himage {ROUTER_DELAY_NODE} tc qdisc del dev {ROUTER_DELAY_IFACE} root")


if __name__ == "__main__":
    main()