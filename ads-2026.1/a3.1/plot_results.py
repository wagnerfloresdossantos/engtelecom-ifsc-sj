import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "results/results.csv"
)

plt.figure(figsize=(8,5))

plt.plot(
    df["lambda"],
    df["theoretical_block"],
    marker="o",
    label="Teórico"
)

plt.plot(
    df["lambda"],
    df["simulated_block"],
    marker="s",
    label="Simulado"
)

plt.xlabel("λ")
plt.ylabel("Probabilidade de Bloqueio")

plt.title(
    "Teoria vs Simulação"
)

plt.grid(True)

plt.legend()

plt.savefig(
    "results/blocking_probability.png"
)

plt.show()