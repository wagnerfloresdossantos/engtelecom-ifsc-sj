import pandas as pd

from simulator import Simulator
from erlang import erlang_b


MU = 1
K = 9

LAMBDAS = [2, 4, 5, 6, 8]

SIM_TIME = 10000

results = []


for lambda_rate in LAMBDAS:

    A = lambda_rate / MU

    sim = Simulator(
        end_time=SIM_TIME,
        lambda_rate=lambda_rate,
        mu=MU,
        k=K
    )

    sim.run()

    sim_results = sim.results()

    theoretical = erlang_b(K, A)

    simulated = sim_results[
        "blocking_probability"
    ]

    error = abs(
        simulated - theoretical
    ) / theoretical

    results.append({

        "lambda": lambda_rate,

        "theoretical_block":
            theoretical,

        "simulated_block":
            simulated,

        "relative_error":
            error,

        "utilization":
            sim_results["utilization"],

        "throughput":
            sim_results["throughput"]

    })


df = pd.DataFrame(results)

print("\n=== RESULTADOS ===\n")

print(df)

df.to_csv(
    "results/results.csv",
    index=False
)

print(
    "\nArquivo salvo em:"
    " results/results.csv"
)