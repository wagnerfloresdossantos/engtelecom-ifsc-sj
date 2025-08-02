import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import komm

from amostragem import amostragem, reconstrucao

def m(t: float) -> float:
    return 6 * np.sin(2*np.pi*t) - 0.0001

def main():
    st.title("Conversão A/D")
    col1, col2 = st.columns(2)
    with col1:
        fa = st.slider(
            label="Taxa de amostragem $f_a$",
            min_value=2,
            max_value=16,
            step=1,
            value=8,
            format="%d amostras/s"
        )
    with col2:
        L = st.select_slider(
            label="Número de níveis de quantização $L:$",
            options=[2,4,8,16,32,64,128,256],
            value=16,

        )
    Ta = 1/fa
    Nb = int(np.log2(L))
    quantizer = komm.UniformQuantizer(
        num_levels=L,
        input_range=(-8,8),
        choice="mid-riser"
    )

    #Curva de quantização
    tab1, tab2, tab3 = st.tabs(["Quantizador", "Sinais", "Tabela"])
    with tab1:
        x = np.linspace(-8, 8, 1000)  ## ARRUMAR!!!!
        y = quantizer.quantize(x)
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title("Curva entrada $\\times$ saída")
        ax.set_xlabel("entrada")
        ax.set_ylabel("saida")
        ax.set_ylim(-8, 8)
        ax.grid()
        st.pyplot(fig)

    # Sinais
    with tab2:
        a, b = (-0.5, 0.5)
        fig, ax = plt.subplots()
        Na = int((b-a) / Ta)
        instantes, amostras = amostragem(m, Ta, a, Na)
        amostras_q =quantizer.quantize(amostras)
        indices = quantizer.digitize(amostras)
        bits = komm.int_to_bits(indices, Nb)
        m_hat = reconstrucao(amostras_q, a, Ta) # type: ignore
        times = np.linspace(a, b, 1000)

        ax.plot(
            times,
            [m(t) for t in times],
            label="$m(t)$",
             color="b"
        )

        ax.plot(
            instantes,
            amostras,
            linestyle="None",
            marker="o",
            label="$m[n]$",
             color="b"
        )

        ax.plot(
            instantes,
            amostras_q,
            linestyle="None",
            marker="o",
            label="$m[q]$",
            color="r"
        )


        ax.plot(
            times,
            [m_hat(t) for t in times],
            label="$\\hat{m}(t)$",
            color = "r"
        )

        ax.grid()
        ax.set_xlabel("$t$ [s]")
        ax.legend()
        st.pyplot(fig)


    with tab3:
        st.table({
            "$t$ [ms]$": [1000*t for t in instantes],
            "$m[t]$ [V]": amostras,
            "$m_q[t] [V]$": amostras_q,
            "indices": indices,
            "bits": ["".join(map(str,reversed(b))) for b in bits],
             
        })
        st.write(bits)




main()