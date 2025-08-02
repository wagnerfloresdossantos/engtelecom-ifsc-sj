import komm
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


def main():
    st.title("Probabilidade de Erro de Bit")
    Rb = 52.36e3 # Taxa de bits em kbps
    Tb = 1/Rb # Período de bit em segundos
    N0 = 2e-4 # Densidade espectral de potência do ruído em W/Hz
    A = 10.0 # Amplitude do sinal V
    sps = 100 # Amostragem por símbolo    n_bits = 100000 # Número de bits a serem simulados
    Eb = A**2 * Tb / 2 # Energia do bit em Joules

    Pb_teo = komm.gaussian_q(np.sqrt(2*Eb/N0)) # Probabilidade de erro de bit
    t = np.arange(0, Tb, step=1/sps) # Eixos de tempo do sinal transmitido
    snr = A**2 / (N0 / 2) # Relação sinal-ruído
    fa = sps * Rb # Frequência de amostragem 
    rng = np.random.default_rng(seed=42) # Gerador de números aleatórios
    bits = dms(n_bits) # Gera os bits
    x_n = 2.0*bits - 1.0 # Mapeia os bits para -1 e 1s
    s_t = A * tx_filter(x_n) # Sinal transmitido
    ts, _ = tx_filter.axes(x_n) # Eixos de tempo do sinal transmitido
    Ts *=Tb # Converte os eixos de tempo para segundos

    # Simulação

    awgn = komm.AWGNChannel(signal_power=A**2, snr = snr/fa, rng=rng) # Canal AWGN)
    r_t = awgn(s_t) # Sinal recebido com ruído 

    n_bits = 10000 # Número de bits a serem simulados
    dms = komm.DiscreteMemorylessSource(pmf=[0.5, 0.5], rng=rng,) # Fonte de bits
    pulse = komm.RectangularPulse(width=0.5) # Pulso retangular
    tx_filter = komm.TransmitFilter(pulse, sps) # Filtro de transmissão
    hr_t = pulse.waveform((Tb - t)/Tb) # Pulso transmitido
    y_t = np.convolve(hr_t, r_t, mode="same") # Convolução do sinal recebido com o filtro de transmissão 
    y_n = y_t[sps-1::sps] # Amostragem do sinal recebido
    bits_hat = (y_n > 0.0).astype(int) # Decisão de bits (0 se y_n < 0, 1 se y_n >= 0)




    fig, ax = plt.subplots(3, 1, figsize=(8, 6))
    ax[0].plot(ts/1e-6, s_t)
    ax[0].set_xlim(0, 10*Tb/1e-6)  # Limita o eixo x para 10 períodos de bit
    ax[0].set_xlabel("Tempo (s)")
    ax[0].set_ylabel("$s(t)$")
    ax[0].set_xtricks(np.arange(0, 1000, 100))
    ax[0].grid()
    ax[1].plot(ts/1e-6, r_t)
    ax[1].set_xlim(0, 10*Tb/1e-6)  # Limita o eixo x para 10 períodos de bit
    ax[1].set_xlabel("Tempo (s)")
    ax[1].set_ylabel("$s(t)$")
    ax[1].set_xtricks(np.arange(0, 1000, 100))
    ax[1].grid()
    ax[2].plot(ts/1e-6, y_t)
    ax[2].set_xlim(0, 10*Tb/1e-6)  # Limita o eixo x para 10 períodos de bit
    ax[2].set_xlabel("Tempo (s)")
    ax[2].set_ylabel("$s(t)$")
    ax[2].set_xtricks(np.arange(0, 1000, 100))
    ax[2].grid()

    fig.tight_layout()
    st.pyplot(fig)

    
    st.metric("$P_b$ teórica", f"{Pb_teo:.9%}")
    st.metric("$P_b$ simulada", f"{Pb_:.9%}")


if __name__ == "__main__":
    main()
