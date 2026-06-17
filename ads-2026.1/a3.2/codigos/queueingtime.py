import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cenarios.csv")

q = df[
    (df["type"] == "histogram") &
    (df["name"] == "queueingTime:histogram")
].copy()

q["cenario"] = q["run"].str.extract(r"^(C\d)")
q = q.dropna(subset=["cenario"])

q["mean_us"] = q["mean"].astype(float) * 1e6

plt.figure(figsize=(8,5))
plt.bar(q["cenario"], q["mean_us"])
plt.xlabel("Cenário")
plt.ylabel("Tempo médio em fila (µs)")
plt.tight_layout()
plt.savefig("grafico_queueingtime_cenarios.png")