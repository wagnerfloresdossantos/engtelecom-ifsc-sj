from typing import Callable
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

type Signal = Callable[[float], float]

def m(t: float) -> float:
    return 2 + 600*np.sinc(200*t) + 8*np.cos(2*np.pi*50*t)

def amostragem(m: Signal, Ta: float, a: float, Na: int) -> tuple[list[float], list[float]]:
    instantes = [a + n*Ta for n in range(Na)]
    amostras = [m(t) for t in instantes]
    return instantes, amostras

def reconstrucao(amostras: list[float], a: float, Ta: float) -> Signal:
    def m_hat(t: float) -> float:
        soma = 0
        for n in range(len(amostras)):
            soma += amostras[n]*np.sinc((t-a)/Ta - n)
        return soma #type: ignore
    return m_hat

def main():
    st.title("Amostragem e reconstrução")
    a, b = -0.1, 0.1
    fa = st.slider(label="Frequência de amostragem [Hz]", 
                   min_value=50, max_value=400, value=200, step = 10)
    Ta = 1/fa
    Na = int((b-a)/Ta)
    instantes, amostras = amostragem(m, Ta, a, Na)
    m_hat = reconstrucao(amostras, a, Ta)
    times = np.linspace(a, b, 1000)
    fig, ax = plt.subplots()
    ax.plot(times, [m(t) for t in times], label="$m(t)$")
    ax.plot(times, [m_hat(t) for t in times], color="red", label="$\\hat{m}(t)$")
    ax.plot(instantes, amostras, linestyle="None", marker="o", color="green", label="$m[n]$")
    ax.set_xlim(a, b)
    ax.set_ylim(-300, 700)
    ax.set_xlabel("$t$ [s]")
    ax.set_ylabel("$m(t)$")
    ax.grid()
    ax.legend()
    st.pyplot(fig)

if __name__ == "__main__":
    main()
