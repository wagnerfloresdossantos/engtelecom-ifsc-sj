from math import sqrt, pi, exp
import komm
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from typing import Callable


def gaussian(x: float) -> float:
    return 1 / sqrt(2*pi) * exp(-x**2 / 2)

def uniform(x: float) -> float:
    return 0.1 if -5 < x < 5 else 0

def laplacian(x: float) -> float:
    return 0.5 * exp(-abs(x))

def gaussian_mixture(x: float) -> float:
    return (
        0.25 * (1/0.5) * gaussian((x + 3) / 0.5) + 
        0.25 * (1/0.5) * gaussian((x - 2) / 0.8) 
    )

def valor_esperado_condicionado(pdf: Callable[[float], float], xi: float, xf: float) -> float:
    xs = np.linspace(xi, xf, 1000)
    num = np.trapezoid([x * pdf(x) for x in xs], xs)
    den = np.trapezoid([pdf(x) for x in xs], xs)
    return num / den # type: ignore

def lloyd_max_step(pdf: Callable, a:float, b:float, L: int, vs:list[float]):
   # Níveis --> Limiares
   ls = [0.0] * (L + 1)
   ls[0] = a
   ls[L] = b
   for i in range(1, L):
       ls[i] = vs[i-1] + vs[i] / 2
   # Limiar --> Nível
   new_vs = [0.0] * L
   for i in range(L):
       new_vs[i] = valor_esperado_condicionado(pdf, ls[i], ls[i+1])
   return ls, vs

def main():
    st.title("Algorithm de Lloyd-Max")
    co1, co2 = st.columns(2)
    with co1:
        L = st.slider(
        label="Número de níveis $L$:",
        min_value=2,
        max_value=20,
        value=4,
        )

    with co2:
        pdf_control = st.segmented_control(
            label="PDF:",
            options=["Uniforme", "Gaussiana", "laplacian", "Gaussian Mixture"],   
            default="Uniforme",

      )
        if pdf_control == "Uniforme":
           pdf = uniform
        elif pdf_control == "Gaussiana":
            pdf = gaussian
        elif pdf_control == "Laplaciana":
            pdf = laplacian
        elif pdf_control == "Gaussian Mixture":
            pdf = gaussian_mixture      
        else:
            raise (ValueError)

        a, b = -5, 5
        vss = list[list[float]] = []
        lss = list[list[float]] = []
        vss.append(list(np.linspace(a, b, L)))
        for i in range(60):
            ls, vs = lloyd_max_step(pdf, a, b, L, vss[i])
            lss.append(ls)
            vss.append(vs)   

    tab1, tab2, tab3 = st.tabs(["PDF", "passo-a-passo", "MSQE"])

    with tab1:
        fig, ax = plt.subplots()
        fig.set_figheight(4)
        xs = np.linspace(-6, 6, 100)
        ax.plot(xs, [pdf(xs) for x in xs])
        for l in lss[-1]:
            ax.axvline(l, color="C2", linestyle="--")
        ax.set_xlabel("$m$")
        ax.set_ylabel("$f_m(m)$")
        ax.set_ylimit(-0.05, 0.55)
        ax.grid()
        st.pyplot(fig)
 
    with tab2:
        for i in range(30):
            ax.plot(lss[i], [i] * [L + 1], linestyle="Nome", marker = "o" color="C2")
            ax.plot(lss[i], [i] * [L + 1], linestyle="Nome", marker = "o" color="C0")

        st.pyplot(fig)
        
        
if __name__ == "__main__":
    main()


