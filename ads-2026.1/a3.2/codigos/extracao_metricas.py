import pandas as pd
from pathlib import Path

CSV_PATH = Path("../data/cenarios.csv")
OUT_PATH = Path("../data/resultados_resumidos.csv")

df = pd.read_csv(CSV_PATH)

# Throughput
throughput = df[
    (df["type"] == "histogram") &
    (df["module"].str.contains("source.eth", na=False)) &
    (df["name"] == "throughput:histogram")
].copy()

throughput["cenario"] = throughput["run"].str.extract(r"^(C\d)")
throughput = throughput.dropna(subset=["cenario"])
throughput["throughput_mbps"] = throughput["mean"].astype(float) / 1e6

# Queueing Time
queue = df[
    (df["type"] == "histogram") &
    (df["name"] == "queueingTime:histogram")
].copy()

queue["cenario"] = queue["run"].str.extract(r"^(C\d)")
queue = queue.dropna(subset=["cenario"])
queue["queueing_time_ms"] = queue["mean"].astype(float) * 1e3

# Resumo
intervalos = {
    "C1": 100,
    "C2": 50,
    "C3": 25,
    "C4": 10,
}

resumo = pd.DataFrame({
    "cenario": ["C1", "C2", "C3", "C4"],
})

resumo["intervalo_us"] = resumo["cenario"].map(intervalos)

resumo = resumo.merge(
    throughput[["cenario", "throughput_mbps"]],
    on="cenario",
    how="left"
)

resumo = resumo.merge(
    queue[["cenario", "queueing_time_ms"]],
    on="cenario",
    how="left"
)

resumo["throughput_mbps"] = resumo["throughput_mbps"].round(2)
resumo["queueing_time_ms"] = resumo["queueing_time_ms"].round(2)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
resumo.to_csv(OUT_PATH, index=False)

print(resumo)
print(f"\nArquivo gerado: {OUT_PATH}")