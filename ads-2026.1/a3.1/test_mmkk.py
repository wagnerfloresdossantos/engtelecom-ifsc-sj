from simulator import Simulator
from erlang import erlang_b


LAMBDA = 5
MU = 1
K = 9

A = LAMBDA / MU

sim = Simulator(
    end_time=10000,
    lambda_rate=LAMBDA,
    mu=MU,
    k=K
)

sim.run()

results = sim.results()

theoretical = erlang_b(K, A)

print("\n=== RESULTADOS ===\n")

print(
    f"Chamadas geradas: "
    f"{results['generated']}"
)

print(
    f"Chamadas aceitas: "
    f"{results['accepted']}"
)

print(
    f"Chamadas bloqueadas: "
    f"{results['blocked']}"
)

print()

print(
    f"Bloqueio simulado: "
    f"{results['blocking_probability']:.6f}"
)

print(
    f"Bloqueio teórico: "
    f"{theoretical:.6f}"
)

print()

print(
    f"Utilização média: "
    f"{results['utilization']:.4f}"
)

print(
    f"Vazão: "
    f"{results['throughput']:.4f}"
)