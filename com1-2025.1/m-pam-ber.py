import komm
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt 

def main():
    st.title("$M$-PAM-BER")
    rng = np.random.default_rng(seed=42)  # Gerador de números aleatórios
    cols = st.columns(2)

    with cols[0]:
        M = st.select_slider(
            label="Ordem da Modulação (M)",
            options=[2, 4, 8, 16]
        )
    with cols[1]:
        labeling = st.radio(
            "Mapeamento",
            ["reflected", "natural"],
            horizontal=True
        )

    mod = komm.PAModulation(M, labeling=labeling)  # Modulador PAM
    k = mod.bits_per_symbol  # Número de bits por símbolo
    n_symbols = 20000  # Número de símbolos a serem simulados
    n_bits = n_symbols * k  # Número de bits a serem simulados
    Rs = 40e3  # Taxa de símbolos em kbaud
    Rb = k * Rs  # Taxa de bits em kbps
    Ts = 1 / Rs  # Período de símbolo em segundos
    A = 4.0  # Amplitude base do sinal V
    Es = A**2 * Ts * (M**2 - 1) / 3  # Energia do símbolo em Joules
    Eb = Es / k  # Energia do bit em Joules
    sps = 100  # Amostragem por símbolo
    fa = sps * Rs  # Frequência de amostragem
    Ta = 1 / fa  # Período de amostragem em segundos
    EbN0_dB_list = np.arange(-8, 9)  # Valores de Eb/N0 em dB
    EbN0_list = 10**(EbN0_dB_list / 10)  # Converte Eb/N0 de dB para linear

    dms = komm.DiscreteMemorylessSource(pmf=[0.5, 0.5], rng=rng)  # Gera os bits
    pulse = komm.RectangularPulse()  # Pulso retangular
    tx_filter = komm.TransmitFilter(pulse, sps)  # Filtro de transmissão

    bits = dms(n_bits)  # Gera os bits
    x_n = mod.modulate(bits)  # Mapeia os bits para símbolos PAM
    s_t = A * tx_filter(x_n)  # Sinal transmitido
    ts, _ = tx_filter.axes(x_n)  # Eixos de tempo do sinal transmitido
    ts *= Ts

    # BER TEÓRICA
    Pb_Teo_list = []  # Lista para armazenar as probabilidades de erro de bit
    for EbN0 in EbN0_list:
        EsN0 = EbN0 * k
        Ps = 2 * (M-1) / M * \
            komm.gaussian_q(np.sqrt(6 / (M**2 - 1)*EsN0))
        Pb = Ps / k  # Probabilidade de erro de bit
        Pb_Teo_list.append(Pb)

    # BER SIMULADA
    Pb_Sim_list = []  # Lista para armazenar as probabilidades de erro de bit simuladas
    for EbN0 in EbN0_list :
        signal_power = Es * Rs  # Potência do sinal
        N0 = Eb / EbN0  # Densidade espectral de potência do ruído
        noise_poower = (N0 / 2) * fa  # Potência do ruído
        snr = signal_power / noise_poower  # Relação sinal-ruído
        awgn = komm.AWGNChannel(signal_power=signal_power, snr=snr, rng=rng,)  # Canal AWGN
        r_t = awgn(s_t)  # Sinal recebido com ruído
        t = np.arange(0, Ts, step = 1/fa)  # Eixos de tempo do sinal recebido
        hr_t = pulse.waveform((Ts - t) / Ts)  # Pulso transmitido
        y_t = np.convolve(hr_t, r_t) / sps  # Convolução do sinal recebido com o filtro de transmissão
        y_t = y_t[:r_t.size]  # Ajusta o tamanho do sinal recebido
        y_n = y_t[sps-1::sps]  # Amostragem do sinal recebido
        bits_hat = mod.demodulate_hard(y_n / A)  # Decisão de bits (0 se y_n < 0, 1 se y_n >= 0)
        Pb = np.mean(bits != bits_hat)  # Probabilidade de erro de bit
        Pb_Sim_list.append(Pb)

    tabs = st.tabs(["Sinais", "BER"])
    with tabs[0]:
        fig, ax = plt.subplots(2, 1, figsize=(6, 4))
        ax[0].plot(ts/1e-6, s_t)
        ax[0].set_xlim(0, 15 * Ts/1e-6) # Limita o eixo x para 15 períodos de símbolo
        ax[0].set_xticks(np.arange(11)*Ts/1e-6)
        ax[0].set_yticks(A*np.arange(-(M-1), M, 2))
        ax[0].set_xlabel("Tempo (ms)")
        ax[0].set_ylabel("$s(t)$")
        ax[0].grid()

        ax[1].plot(ts/1e-6, y_t) # type: ignore
        ax[1].set_xlim(0, 15 * Ts/1e-6) # Limita o eixo x para 15 períodos de símbolo
        ax[1].set_xticks(np.arange(11)*Ts/1e-6)
        ax[1].set_yticks(A*np.arange(-(M-1), M, 2))
        ax[1].set_xlabel("Tempo (ms)")
        ax[1].set_ylabel("$s(t)$")
        ax[1].grid()
        fig.tight_layout()
        st.pyplot(fig)
    with tabs[1]:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.semilogy(EbN0_dB_list, Pb_Teo_list, label="Teórica")
        ax.semilogy(EbN0_dB_list, Pb_Sim_list, label="Simulada")
        ax.set_xlabel("$E_b/N_0$ (dB)")
        ax.set_ylabel("$P_b$")
        ax.grid()
        fig.tight_layout()
        st.pyplot(fig)


    
    
if __name__ == "__main__":    
    main()

