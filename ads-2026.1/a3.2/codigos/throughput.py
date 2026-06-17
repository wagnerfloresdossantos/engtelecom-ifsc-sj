import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cenarios.csv")

h = df[
    (df["type"] == "histogram") &
    (df["module"].str.contains("source.eth", na=False)) &
    (df["name"] == "throughput:histogram")
].copy()

h["cenario"] = h["run"].str.extract(r"^(C\d)")
h = h.dropna(subset=["cenario"])

h["mean_Mbps"] = h["mean"].astype(float) / 1e6

plt.figure(figsize=(8,5))
plt.bar(h["cenario"], h["mean_Mbps"])
plt.xlabel("Cenário")
plt.ylabel("Throughput médio (Mbps)")
plt.tight_layout()
plt.savefig("grafico_throughput_cenarios.png")