#!/usr/bin/env python3
"""
Script de análise dos resultados do planejamento fatorial 2^2.

Entrada:
  - resultados_imunes/resultados.csv

Saídas geradas:
  - resultados_imunes/sumario_iperf_avg_mbps.csv
  - resultados_imunes/sumario_retrans_rate.csv
  - resultados_imunes/sumario_retrans_rate_extendido.csv   <-- NOVO (mediana, %>0, R_agg)
  - resultados_imunes/efeitos_2x2.csv
  - resultados_imunes/figuras/throughput_means_ci95.png
  - resultados_imunes/figuras/retrans_rate_means_ci95.png
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import t

CSV_PATH = Path("resultados_imunes/resultados.csv")
OUT_DIR = Path("resultados_imunes")
FIG_DIR = OUT_DIR / "figuras"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def summarize_response(df: pd.DataFrame, ycol: str) -> pd.DataFrame:
    """
    Resume uma variável de resposta (ycol) por tratamento (alg, delay_ms).
    Retorna: n, mean, sd, ci95_half, ci95_low, ci95_high.
    """
    g = df.groupby(["alg", "delay_ms"])[ycol]
    n = g.count()
    mean = g.mean()
    sd = g.std(ddof=1)

    se = sd / np.sqrt(n)
    tcrit = t.ppf(0.975, n - 1)  # IC95 bicaudal
    ci = tcrit * se

    out = pd.DataFrame({
        "alg": mean.index.get_level_values(0),
        "delay_ms": mean.index.get_level_values(1),
        "n": n.values,
        "mean": mean.values,
        "sd": sd.values,
        "ci95_half": ci.values,
        "ci95_low": (mean - ci).values,
        "ci95_high": (mean + ci).values,
    })
    return out


def summarize_retrans_extended(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sumário "honesto" para retransmissão quando há muitos zeros:

    - mediana do retrans_rate (robusta a cauda/zeros)
    - pct_retrans_gt0: % de execuções com n_retrans > 0
    - R_agg: soma(n_retrans) / soma(n_dados)  (melhor que média de taxas)
    - mantém também mean/sd/IC95 do retrans_rate (para comparação)
    """
    # 1) Base clássica (mean/sd/IC95) do retrans_rate
    base = summarize_response(df, "retrans_rate")

    # 2) Mediana do retrans_rate
    med = df.groupby(["alg", "delay_ms"])["retrans_rate"].median().rename("median").reset_index()

    # 3) % de execuções com retrans > 0
    tmp = df.copy()
    tmp["has_retrans"] = tmp["n_retrans"] > 0
    pct = (tmp.groupby(["alg", "delay_ms"])["has_retrans"].mean() * 100.0).rename("pct_retrans_gt0").reset_index()

    # 4) R_agg = sum(n_retrans)/sum(n_dados)
    agg = df.groupby(["alg", "delay_ms"]).agg(
        n_dados_sum=("n_dados", "sum"),
        n_retrans_sum=("n_retrans", "sum"),
    ).reset_index()
    agg["R_agg"] = np.where(agg["n_dados_sum"] > 0, agg["n_retrans_sum"] / agg["n_dados_sum"], np.nan)

    # 5) Merge final
    out = base.merge(med, on=["alg", "delay_ms"], how="left") \
              .merge(pct, on=["alg", "delay_ms"], how="left") \
              .merge(agg, on=["alg", "delay_ms"], how="left")

    # organização das colunas (mais legível)
    cols = [
        "alg", "delay_ms",
        "n",
        "mean", "sd", "ci95_half", "ci95_low", "ci95_high",
        "median", "pct_retrans_gt0",
        "n_dados_sum", "n_retrans_sum", "R_agg",
    ]
    return out[cols].sort_values(["alg", "delay_ms"])


def factorial_effects(df: pd.DataFrame, ycol: str, a_low="reno", a_high="cubic", d_low=10, d_high=50) -> dict:
    """
    Efeitos do planejamento 2^2 com codificação -1/+1.
    """
    cell = df.groupby(["alg", "delay_ms"])[ycol].mean().reset_index()
    cell["xA"] = cell["alg"].map({a_low: -1, a_high: 1})
    cell["xD"] = cell["delay_ms"].map({d_low: -1, d_high: 1})
    cell["xAD"] = cell["xA"] * cell["xD"]

    b0 = cell[ycol].mean()
    bA = (cell["xA"] * cell[ycol]).sum() / 4
    bD = (cell["xD"] * cell[ycol]).sum() / 4
    bAD = (cell["xAD"] * cell[ycol]).sum() / 4

    return {
        "b0": b0, "bA": bA, "bD": bD, "bAD": bAD,
        "effect_A": 2 * bA,
        "effect_D": 2 * bD,
        "effect_AD": 2 * bAD,
        "cell_means": cell.sort_values(["alg", "delay_ms"]),
    }


def plot_means_ci(summary_df, y_label, title, outpath, logy=False):
    algs = sorted(summary_df["alg"].unique())
    delays = sorted(summary_df["delay_ms"].unique())
    x = np.arange(len(delays))
    width = 0.35 if len(algs) == 2 else 0.8 / len(algs)

    fig, ax = plt.subplots(figsize=(7, 4.2), constrained_layout=True)

    for i, alg in enumerate(algs):
        sub = summary_df[summary_df["alg"] == alg].sort_values("delay_ms")
        offs = (i - (len(algs) - 1) / 2) * width
        ax.errorbar(x + offs, sub["mean"], yerr=sub["ci95_half"], fmt="o-", capsize=4, label=alg)

    ax.set_xticks(x)
    ax.set_xticklabels([f"{d} ms" for d in delays])
    ax.set_xlabel("Delay (fator D)")
    ax.set_ylabel(y_label)
    ax.set_title(title)

    if logy:
        ax.set_yscale("log")

    ax.legend(title="Algoritmo (fator A)")

    # ESSENCIAL pra não cortar nada:
    fig.savefig(outpath, dpi=200, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


def main():
    df = pd.read_csv(CSV_PATH)
    df["alg"] = df["alg"].astype(str).str.lower()
    df["delay_ms"] = df["delay_ms"].astype(int)

    # Sumários clássicos
    sum_thr = summarize_response(df, "iperf_avg_mbps")
    sum_ret = summarize_response(df, "retrans_rate")

    # Sumário estendido (retrans)
    sum_ret_ext = summarize_retrans_extended(df)

    # Gráficos
    plot_means_ci(
        sum_thr,
        "Vazão média (Mbit/s)",
        "Médias por tratamento (IC 95%) — iperf_avg_mbps",
        FIG_DIR / "throughput_means_ci95.png",
        logy=False,
    )
    plot_means_ci(
        sum_ret,
        "Taxa de retransmissão (retrans/segmento)",
        "Médias por tratamento (IC 95%) — retrans_rate",
        FIG_DIR / "retrans_rate_means_ci95.png",
        logy=True,
    )

    # Salvar CSVs
    sum_thr.to_csv(OUT_DIR / "sumario_iperf_avg_mbps.csv", index=False)
    sum_ret.to_csv(OUT_DIR / "sumario_retrans_rate.csv", index=False)
    sum_ret_ext.to_csv(OUT_DIR / "sumario_retrans_rate_extendido.csv", index=False)

    # Efeitos (mantendo como antes: effects sobre as MÉDIAS de ycol)
    eff_thr = factorial_effects(df, "iperf_avg_mbps")
    eff_ret = factorial_effects(df, "retrans_rate")

    pd.DataFrame([{
        "y": "iperf_avg_mbps",
        "effect_A": eff_thr["effect_A"],
        "effect_D": eff_thr["effect_D"],
        "effect_AD": eff_thr["effect_AD"],
    }, {
        "y": "retrans_rate",
        "effect_A": eff_ret["effect_A"],
        "effect_D": eff_ret["effect_D"],
        "effect_AD": eff_ret["effect_AD"],
    }]).to_csv(OUT_DIR / "efeitos_2x2.csv", index=False)

    print("OK!")
    print("Gráficos em:", FIG_DIR)
    print("Sumários em:", OUT_DIR)
    print("Sumário estendido (retrans) em:", OUT_DIR / "sumario_retrans_rate_extendido.csv")


if __name__ == "__main__":
    main()