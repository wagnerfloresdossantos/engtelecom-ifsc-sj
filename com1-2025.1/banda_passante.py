import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

def main():
    st.title("Modulação em Banda Passante")

    M = 4
    k = 2
    Rs = 20e3
    Ts = 1 / Rs
    sps = 500
    fa = sps * Rs  # Frequência de amostragem
    fc = 160e3  # Frequência de corte do filtro

    mod_radio = st.radio(
        label="Tipo de Modulação",
        options=["ASK", "PSK", "FSK"],
        horizontal=True, 
    )

    def ask_mod():
        s_t = np.zeros_like(t)  # Sinal transmitido
        amplitudes = [0, 1, 2, 3]  # Amplitude do sinal ASK
        for i, s in enumerate(symbols):
            A = amplitudes[s]
            idx = slice(i * sps, (i + 1) * sps)
            s_t[idx] = A * np.cos(2 * np.pi * fc * t[idx])
        return s_t
    
    def psk_mod():
        s_t = np.zeros_like(t)  # Sinal transmitido
        phases = [0, np.pi/2, np.pi, 3*np.pi/2]  # Fase do sinal PSK
        for i, s in enumerate(symbols):
            phi = phases[s]
            idx = slice(i * sps, (i + 1) * sps)
            s_t[idx] = np.cos(2 * np.pi * fc * t[idx] - phi)
        return s_t
    
    def fsk_mod():
        s_t = np.zeros_like(t)  # Sinal transmitido
        delta_f = 40e3
        freqs = [fc + n*delta_f for n in range(-3, -1, 1, 3)]  # Frequências FSK         
     

        for i, s in enumerate(symbols):
            fi = freqs[s]
            idx = slice(i * sps, (i + 1) * sps)
            s_t[idx] = np.cos(2 * np.pi * fc * t[idx])
        return s_t

    bits = np.array([0, 1, 0, 1, 1, 1, 0, 0, 1, 0])  # Exemplo de sequência de
    mum_bits = len(bits)  # Número de bits
    n_symbols = mum_bits // k  # Número de símbolos
    st.write(f"Bistos: `{bits}`")

    # Mapeamento dos bits para símbolos
    gray = {
        (0, 0): 0,
        (0, 1): 1,
        (1, 1): 2,
        (1, 0): 3
    }
    bits_reshaped = bits.reshape(-1, k)
    symbols = np.array(
        [gray[tuple(k)] for k in bits_reshaped]
    )
    st.write(f"Símbolos: `{symbols}`")

    t = np.arange(0, n_symbols * Ts, 1 / fa)  # Eixo de tempo

    if mod_radio == "ASK":
        s_t = ask_mod()
    elif mod_radio == "PSK":
        s_t = psk_mod()
    elif mod_radio == "FSK":
        s_t = fsk_mod()

    s_t = np.zeros_like(t)  # Sinal transmitido
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(t/1e-6, s_t, label="Sinal Transmitido", color="blue")
    ax.set_xlabel("Tempo (us)")
    ax.set_ylabel("Amplitude (S(t))")
    ax.grid()
    st.pyplot(fig)


if __name__ == "__main__":
    main()
  


