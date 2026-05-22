import math


def erlang_b(k, A):
    """
    Fórmula de Erlang-B

    k -> número de canais
    A -> carga oferecida
    """

    numerator = (A ** k) / math.factorial(k)

    denominator = 0

    for i in range(k + 1):
        denominator += (A ** i) / math.factorial(i)

    return numerator / denominator