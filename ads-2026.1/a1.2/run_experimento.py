#!/usr/bin/env python3
"""
Automação do experimento fatorial 2^2 no IMUNES.

Topologia:
  TCP principal: pc1 (10.0.0.20)  --->  pc2 (10.0.2.20)
  UDP background: pc4 (10.0.4.20) --->  pc3 (10.0.3.20)

Fatores:
  A: algoritmo TCP (reno / cubic) aplicado no pc1
  D: delay (10 / 50 ms) aplicado no enlace entre roteadores (router1, eth1)

Respostas:
  - vazão média via iperf (Mbit/s)
  - taxa de retransmissão via tshark

Recursos desta versão:
  - logs em arquivo e no terminal
  - captura apenas do fluxo TCP principal
  - timeout no tcpdump
  - snaplen reduzido
  - limite de tamanho do pcap (-C) e um único arquivo (-W 1)
  - limpeza automática mesmo com erro/interrupção
  - retomada segura: não reexecuta combinações já presentes no CSV
"""

import atexit
import csv
import logging
import re
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Iterable

# =========================
# TOPOLOGIA
# =========================

TCP_CLIENT = "pc1"
TCP_SERVER = "pc2"
TCP_CLIENT_IP = "10.0.0.20"
TCP_SERVER_IP = "10.0.2.20"

UDP_CLIENT = "pc4"
UDP_SERVER = "pc3"
UDP_CLIENT_IP = "10.0.4.20"
UDP_SERVER_IP = "10.0.3.20"

CAPTURE_NODE = "router1"
CAPTURE_IFACE = "eth1"

ROUTER_DELAY_NODE = "router1"
ROUTER_DELAY_IFACE = "eth1"

# =========================
# PARÂMETROS FIXOS
# =========================

DURACAO_IPERF_S = 30
BG_UDP_MBPS = 900
IPERF_TCP_PORT = 5001
IPERF_UDP_PORT = 5002

ALGS = ["reno", "cubic"]
DELAYS_MS = [10, 50]
REPS = 8

# Proteções
TCPDUMP_TIMEOUT_S = 45
TCPDUMP_SNAPLEN = 128
TCPDUMP_MAX_MB = 20
CMD_TIMEOUT_S = 90

# Diretórios
OUTDIR = Path("resultados_imunes")
FIGDIR = OUTDIR / "figuras"
LOGDIR = OUTDIR / "logs"
OUTDIR.mkdir(exist_ok=True)
FIGDIR.mkdir(exist_ok=True)
LOGDIR.mkdir(exist_ok=True)

CSV_PATH = OUTDIR / "resultados.csv"
LOG_PATH = LOGDIR / "run_experimento.log"

# Estado global para cleanup em saída anormal
_STOPPING = False


# =========================
# LOGGING
# =========================

def setup_logging() -> logging.Logger:
    logger = logging.getLogger("run_experimento")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    fh = logging.FileHandler(LOG_PATH, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


LOGGER = setup_logging()


# =========================
# EXECUÇÃO DE COMANDOS
# =========================

def sh(cmd: str, check: bool = True, timeout: int | None = None) -> str:
    LOGGER.info("$ %s", cmd)
    try:
        p = subprocess.run(
            cmd,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"Timeout executando comando: {cmd}") from exc

    out = p.stdout or ""
    if check and p.returncode != 0:
        raise RuntimeError(f"Falhou ({p.returncode}): {cmd}\n---\n{out}\n---")
    return out


def himage(node: str, cmd: str, check: bool = True, timeout: int | None = None) -> str:
    return sh(f"sudo himage {node} {cmd}", check=check, timeout=timeout)


def himage_nc(node: str, cmd: str) -> str:
    return himage(node, cmd, check=False)


def hcp(src: str, dst: str) -> None:
    sh(f"sudo hcp {src} {dst}", check=True, timeout=CMD_TIMEOUT_S)


# =========================
# LIMPEZA / ENCERRAMENTO
# =========================

def cleanup_udp_client() -> None:
    himage_nc(UDP_CLIENT, r"""sh -lc '
        pid=$(cat /tmp/iperf_udp_client.pid 2>/dev/null || true)
        case "$pid" in
            (""|*[!0-9]*) true ;;
            (*) kill -INT "$pid" 2>/dev/null || true; sleep 0.3; kill -9 "$pid" 2>/dev/null || true ;;
        esac
        pkill -f "iperf -c .* -u -p 5002" 2>/dev/null || true
        rm -f /tmp/iperf_udp_client.pid /tmp/iperf_udp_client.log 2>/dev/null || true
    '""")


def cleanup_tcpdump() -> None:
    himage_nc(CAPTURE_NODE, r"""sh -lc '
        pid=$(cat /tmp/tcpdump.pid 2>/dev/null || true)
        case "$pid" in
            (""|*[!0-9]*) true ;;
            (*) kill -INT "$pid" 2>/dev/null || true; sleep 0.3; kill -9 "$pid" 2>/dev/null || true ;;
        esac
        pkill -f "tcpdump.*-w /tmp/" 2>/dev/null || true
        rm -f /tmp/tcpdump.pid /tmp/tcpdump.log 2>/dev/null || true
    '""")


def cleanup_capture_files() -> None:
    himage_nc(CAPTURE_NODE, r"""sh -lc '
        rm -f /tmp/*.pcap /tmp/*.pcap[0-9]* /tmp/tcpdump* 2>/dev/null || true
    '""")


def cleanup_all() -> None:
    global _STOPPING
    if _STOPPING:
        return
    _STOPPING = True
    LOGGER.info("Iniciando limpeza global...")
    try:
        cleanup_udp_client()
    except Exception as e:
        LOGGER.warning("Falha ao limpar UDP client: %s", e)
    try:
        cleanup_tcpdump()
    except Exception as e:
        LOGGER.warning("Falha ao limpar tcpdump: %s", e)
    try:
        cleanup_capture_files()
    except Exception as e:
        LOGGER.warning("Falha ao limpar arquivos de captura: %s", e)
    LOGGER.info("Limpeza global concluída.")


def _signal_handler(signum, frame):
    LOGGER.warning("Sinal recebido (%s). Encerrando com limpeza...", signum)
    cleanup_all()
    sys.exit(1)


atexit.register(cleanup_all)
signal.signal(signal.SIGINT, _signal_handler)
signal.signal(signal.SIGTERM, _signal_handler)


# =========================
# PREPARAÇÃO DOS SERVIDORES
# =========================

def ensure_tcp_server() -> None:
    himage_nc(TCP_SERVER, r"""sh -lc '
        pid=$(cat /tmp/iperf_tcp.pid 2>/dev/null || true)
        case "$pid" in
            (""|*[!0-9]*) true ;;
            (*) kill -9 "$pid" 2>/dev/null || true ;;
        esac
        pkill -f "iperf -s -p 5001" 2>/dev/null || true
        rm -f /tmp/iperf_tcp.pid /tmp/iperf_tcp.log
    '""")

    himage(TCP_SERVER, rf"""sh -lc '
        nohup iperf -s -p {IPERF_TCP_PORT} >/tmp/iperf_tcp.log 2>&1 </dev/null &
        echo $! > /tmp/iperf_tcp.pid
        sleep 0.3
    '""", timeout=CMD_TIMEOUT_S)

    out = himage(TCP_SERVER, rf"""sh -lc '
        pid=$(cat /tmp/iperf_tcp.pid 2>/dev/null || true)
        case "$pid" in (""|*[!0-9]*) exit 1 ;; esac
        kill -0 "$pid" 2>/dev/null || exit 1
        ss -lnt | grep -q ":{IPERF_TCP_PORT}" && echo OK || exit 1
    '""", timeout=CMD_TIMEOUT_S)

    if "OK" not in out:
        raise RuntimeError("Servidor TCP iperf não subiu corretamente no pc2.")


def ensure_udp_server() -> None:
    himage_nc(UDP_SERVER, r"""sh -lc '
        pid=$(cat /tmp/iperf_udp.pid 2>/dev/null || true)
        case "$pid" in
            (""|*[!0-9]*) true ;;
            (*) kill -9 "$pid" 2>/dev/null || true ;;
        esac
        pkill -f "iperf -s -u -p 5002" 2>/dev/null || true
        rm -f /tmp/iperf_udp.pid /tmp/iperf_udp.log
    '""")

    himage(UDP_SERVER, rf"""sh -lc '
        nohup iperf -s -u -p {IPERF_UDP_PORT} >/tmp/iperf_udp.log 2>&1 </dev/null &
        echo $! > /tmp/iperf_udp.pid
        sleep 0.3
    '""", timeout=CMD_TIMEOUT_S)

    out = himage(UDP_SERVER, rf"""sh -lc '
        pid=$(cat /tmp/iperf_udp.pid 2>/dev/null || true)
        case "$pid" in (""|*[!0-9]*) exit 1 ;; esac
        kill -0 "$pid" 2>/dev/null || exit 1
        ss -lun | grep -q ":{IPERF_UDP_PORT}" && echo OK || exit 1
    '""", timeout=CMD_TIMEOUT_S)

    if "OK" not in out:
        raise RuntimeError("Servidor UDP iperf não subiu corretamente no pc3.")


# =========================
# CONFIGURAÇÃO DOS FATORES
# =========================

def set_tcp_cc(alg: str) -> None:
    himage(
        TCP_CLIENT,
        f"sh -lc 'sysctl -w net.ipv4.tcp_congestion_control={alg} >/dev/null'",
        timeout=CMD_TIMEOUT_S
    )


def clear_delay() -> None:
    himage_nc(
        ROUTER_DELAY_NODE,
        f"sh -lc 'tc qdisc del dev {ROUTER_DELAY_IFACE} root 2>/dev/null || true'"
    )


def set_delay_ms(delay_ms: int) -> None:
    add_cmd = f"tc qdisc add dev {ROUTER_DELAY_IFACE} root netem delay {delay_ms}ms"
    chg_cmd = f"tc qdisc change dev {ROUTER_DELAY_IFACE} root netem delay {delay_ms}ms"
    himage(
        ROUTER_DELAY_NODE,
        f"sh -lc '{add_cmd} || {chg_cmd}'",
        timeout=CMD_TIMEOUT_S
    )


# =========================
# BACKGROUND UDP
# =========================

def start_udp_background(duration_s: int, rate_mbps: int) -> None:
    cleanup_udp_client()
    himage(UDP_CLIENT, rf"""sh -lc '
        nohup iperf -c {UDP_SERVER_IP} -u -p {IPERF_UDP_PORT} -b {rate_mbps}M -t {duration_s} \
            >/tmp/iperf_udp_client.log 2>&1 </dev/null &
        echo $! > /tmp/iperf_udp_client.pid
        sleep 1
        pid=$(cat /tmp/iperf_udp_client.pid 2>/dev/null || true)
        case "$pid" in (""|*[!0-9]*) echo FAIL; exit 1 ;; esac
        kill -0 "$pid" 2>/dev/null && echo OK || (echo FAIL; cat /tmp/iperf_udp_client.log; exit 1)
    '""", timeout=CMD_TIMEOUT_S)


# =========================
# CAPTURA
# =========================

def start_tcpdump(pcap_node: str) -> None:
    """
    Captura apenas o fluxo TCP principal.
    Proteções:
      - timeout
      - snaplen curto
      - limite de 20 MB por arquivo
      - apenas um arquivo rotativo
    """
    cleanup_tcpdump()

    tcp_filter = (
        f"tcp and host {TCP_CLIENT_IP} and host {TCP_SERVER_IP} and port {IPERF_TCP_PORT}"
    )

    cmd = (
        f"rm -f {pcap_node} {pcap_node}[0-9]* /tmp/tcpdump.pid /tmp/tcpdump.log; "
        f"nohup timeout {TCPDUMP_TIMEOUT_S} "
        f"tcpdump -U -Z root -s {TCPDUMP_SNAPLEN} -C {TCPDUMP_MAX_MB} -W 1 "
        f"-i {CAPTURE_IFACE} -w {pcap_node} "
        f"'{tcp_filter}' "
        f">/tmp/tcpdump.log 2>&1 </dev/null & "
        f"sleep 0.5; "
        f"pgrep -f \"tcpdump.*-w {pcap_node}\" | tail -n 1 > /tmp/tcpdump.pid; "
        f"pid=$(cat /tmp/tcpdump.pid 2>/dev/null); "
        f"case \"$pid\" in (\"\"|*[!0-9]*) echo FAIL; cat /tmp/tcpdump.log; exit 1 ;; esac; "
        f"kill -0 \"$pid\" 2>/dev/null && echo OK || "
        f"(echo FAIL; cat /tmp/tcpdump.log; exit 1)"
    )
    himage(CAPTURE_NODE, f"sh -lc \"{cmd}\"", timeout=CMD_TIMEOUT_S)


def stop_tcpdump(pcap_node: str) -> None:
    himage(CAPTURE_NODE, f"""sh -lc '
        pid=$(cat /tmp/tcpdump.pid 2>/dev/null || true)
        case "$pid" in (""|*[!0-9]*) exit 0 ;; esac

        kill -INT "$pid" 2>/dev/null || true

        for i in $(seq 1 50); do
            kill -0 "$pid" 2>/dev/null || break
            sleep 0.1
        done

        kill -0 "$pid" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true

        # Espera o arquivo estabilizar
        target=""
        for cand in "{pcap_node}" "{pcap_node}0"; do
            [ -f "$cand" ] && target="$cand" && break
        done

        [ -n "$target" ] || exit 1

        last=-1
        for i in $(seq 1 30); do
            sz=$(stat -c %s "$target" 2>/dev/null || echo 0)
            [ "$sz" -eq "$last" ] && break
            last="$sz"
            sleep 0.1
        done

        test -s "$target" || (echo "PCAP vazio"; cat /tmp/tcpdump.log; exit 1)
    '""", timeout=CMD_TIMEOUT_S)


def detect_remote_pcap_path(pcap_node: str) -> str:
    out = himage(CAPTURE_NODE, f"""sh -lc '
        for cand in "{pcap_node}" "{pcap_node}0"; do
            if [ -s "$cand" ]; then
                echo "$cand"
                exit 0
            fi
        done
        exit 1
    '""", timeout=CMD_TIMEOUT_S)
    return out.strip().splitlines()[-1].strip()


# =========================
# EXTRAÇÃO DE MÉTRICAS
# =========================

def parse_iperf_mbps(iperf_out: str) -> float:
    matches = re.findall(r'([0-9]*\.?[0-9]+)\s+(Kbits/sec|Mbits/sec|Gbits/sec)', iperf_out)
    if not matches:
        raise RuntimeError(f"Não achei taxa no iperf:\n{iperf_out}")

    val_str, unit = matches[-1]
    val = float(val_str)

    if unit == "Kbits/sec":
        return val / 1000.0
    if unit == "Mbits/sec":
        return val
    if unit == "Gbits/sec":
        return val * 1000.0
    raise RuntimeError(f"Unidade inesperada no iperf: {unit}")


def tshark_count(pcap_path: Path, display_filter: str) -> int:
    cmd = f'tshark -n -r "{pcap_path}" -Y "{display_filter}" 2>/dev/null | wc -l'
    out = sh(cmd, timeout=CMD_TIMEOUT_S)
    return int(out.strip())


def tshark_sum_tcp_payload_bytes(pcap_path: Path, display_filter: str) -> int:
    cmd = f'tshark -n -r "{pcap_path}" -Y "{display_filter}" -T fields -e tcp.len 2>/dev/null'
    out = sh(cmd, check=False, timeout=CMD_TIMEOUT_S)
    total = 0
    for line in out.splitlines():
        line = line.strip()
        if line.isdigit():
            total += int(line)
    return total


# =========================
# RETOMADA SEGURA
# =========================

def load_completed_runs(csv_path: Path) -> set[tuple[str, int, int]]:
    if not csv_path.exists():
        return set()

    completed: set[tuple[str, int, int]] = set()
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                completed.add((
                    str(row["alg"]).strip().lower(),
                    int(row["delay_ms"]),
                    int(row["rep"]),
                ))
            except Exception:
                continue
    return completed


def iter_runs() -> Iterable[tuple[str, int, int]]:
    for alg in ALGS:
        for delay in DELAYS_MS:
            for rep in range(1, REPS + 1):
                yield alg, delay, rep


# =========================
# UMA EXECUÇÃO
# =========================

def run_one(alg: str, delay_ms: int, rep: int) -> dict:
    ts = datetime.now().isoformat(timespec="seconds")
    pcap_name = f"{alg}_{delay_ms}ms_rep{rep}.pcap"
    pcap_node = f"/tmp/{pcap_name}"
    pcap_host = OUTDIR / pcap_name

    LOGGER.info("RUN START | alg=%s delay=%sms rep=%s", alg, delay_ms, rep)

    t0 = time.time()
    try:
        set_delay_ms(delay_ms)
        set_tcp_cc(alg)

        cleanup_udp_client()
        cleanup_tcpdump()
        cleanup_capture_files()

        start_udp_background(DURACAO_IPERF_S + 3, BG_UDP_MBPS)
        start_tcpdump(pcap_node)
        time.sleep(1)

        iperf_out = himage(
            TCP_CLIENT,
            f"sh -lc 'iperf -c {TCP_SERVER_IP} -p {IPERF_TCP_PORT} -t {DURACAO_IPERF_S}'",
            check=False,
            timeout=CMD_TIMEOUT_S
        )
        mbps = parse_iperf_mbps(iperf_out)

        stop_tcpdump(pcap_node)
        remote_pcap = detect_remote_pcap_path(pcap_node)
        hcp(f"{CAPTURE_NODE}:{remote_pcap}", str(pcap_host))

        tcp_base_filter = (
            f"ip.src=={TCP_CLIENT_IP} and ip.dst=={TCP_SERVER_IP} and tcp.dstport=={IPERF_TCP_PORT}"
        )

        total = tshark_count(pcap_host, f"{tcp_base_filter} and tcp.len>0")
        retrans = tshark_count(
            pcap_host,
            f"{tcp_base_filter} and tcp.len>0 and "
            f"(tcp.analysis.retransmission or tcp.analysis.fast_retransmission)"
        )
        payload_bytes = tshark_sum_tcp_payload_bytes(
            pcap_host,
            f"{tcp_base_filter} and tcp.len>0"
        )
        retrans_rate = (retrans / total) if total > 0 else 0.0

        elapsed = time.time() - t0
        LOGGER.info(
            "RUN OK | alg=%s delay=%sms rep=%s | vazao=%.3f Mbps | n_dados=%d | n_retrans=%d | retrans_rate=%.6f | %.1fs",
            alg, delay_ms, rep, mbps, total, retrans, retrans_rate, elapsed
        )

        return {
            "timestamp": ts,
            "rep": rep,
            "alg": alg,
            "delay_ms": delay_ms,
            "bg_udp_mbps": BG_UDP_MBPS,
            "iperf_avg_mbps": mbps,
            "tcp_payload_bytes": payload_bytes,
            "n_dados": total,
            "n_retrans": retrans,
            "retrans_rate": retrans_rate,
            "pcap_file": pcap_name,
        }

    finally:
        cleanup_udp_client()
        cleanup_tcpdump()
        cleanup_capture_files()
        pcap_host.unlink(missing_ok=True)


# =========================
# MAIN
# =========================

def main() -> None:
    LOGGER.info("===== INÍCIO DO EXPERIMENTO =====")

    ensure_tcp_server()
    ensure_udp_server()
    clear_delay()

    cleanup_udp_client()
    cleanup_tcpdump()
    cleanup_capture_files()

    completed = load_completed_runs(CSV_PATH)
    LOGGER.info("Execuções já presentes no CSV: %d", len(completed))

    write_header = not CSV_PATH.exists()
    total_runs = len(list(iter_runs()))
    remaining_runs = total_runs - len(completed)
    LOGGER.info("Total planejado: %d | Restantes: %d", total_runs, remaining_runs)

    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "timestamp", "rep", "alg", "delay_ms", "bg_udp_mbps",
                "iperf_avg_mbps", "tcp_payload_bytes",
                "n_dados", "n_retrans", "retrans_rate", "pcap_file"
            ]
        )
        if write_header:
            writer.writeheader()

        for alg, delay, rep in iter_runs():
            key = (alg, delay, rep)
            if key in completed:
                LOGGER.info("SKIP | alg=%s delay=%sms rep=%s já existe no CSV", alg, delay, rep)
                continue

            try:
                row = run_one(alg, delay, rep)
                writer.writerow(row)
                f.flush()
            except Exception as e:
                LOGGER.exception(
                    "RUN FAIL | alg=%s delay=%sms rep=%s | erro=%s",
                    alg, delay, rep, e
                )
                raise

    clear_delay()
    cleanup_all()

    LOGGER.info("CSV salvo em: %s", CSV_PATH)
    LOGGER.info("Log salvo em: %s", LOG_PATH)
    LOGGER.info("===== FIM DO EXPERIMENTO =====")


if __name__ == "__main__":
    main()