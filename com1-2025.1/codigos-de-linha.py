import numpy as np
import matplotlib.pylab as plt
import streamlit as st
import komm
import komm.abc
from numpy.fft import fft, fftshift

def polarmapping(bn):
    xn = 2.0*bn -1.0
    return xn

def on_of_mapping(bn):
    xn = 1.0*bin
    return xn

def ami_mapping(bn):
    xn = np.zeros_like(bn, dtype=float)
    idx = np.where(bn)
    i = np.arange(idx.size)
    xn[idx] = (-1)**i
    return xn

A = 1.0
Tb = 1.0

def main():
    pulse_menu = {
        "Retangula NRZ": komm.RectangularPulse(1),
        "Retangular RZ": komm.RectangularPulse(0.5),
        "Manchester": komm.ManchesterPulse(),      
    }
    mapping_menu = {
        "Polar": polarmapping,
        "On-Off": on_of_mapping,
        "AMI": ami_mapping,
    }
    st.title("Códigos de linha")
    pulse_choice = st.segmented_control(
        label = "Pulso",
        options=pulse_menu.keys(),
        default="Retangular NRZ",
    )
    mapping_choice = st.segmented_control(
        label = "Mapeamento",
        options=mapping_menu.keys(),
        default="Polar",
    )
    if mapping_choice is None or mapping_choice not in mapping_menu:
        raise Exception("Selecione um mapeamento")
    
    if pulse_choice is None or pulse_choice not in pulse_menu:
        raise Exception("Selecione um pulso")
    
    match (mapping_choice, pulse_choice):
        case ("Polar", "Retangular NRZ"):
            psd_teo = lambda f: A**2 * Tb * np.sinc(f*Tb)**2
        case ("on-off", "Retangular NRZ"):
            # Sem os impulsos
            pdd_teo = lambda f: A**2 * Tb / 16  * np.sinc(Tb * f/2)**2
        case ("Polar", "Manchester"):
            psd_teo = lambda f: A**2 * Tb * np.sinc(f*Tb)**2 * np.sin(2*np.pi * Tb/4 * f)**2
        case _: 
            raise ValueError("Combinacao de mapeamento e pulso não suportada")
    
    pulse : komm.abc.Pulse = pulse_menu[pulse_choice]    
    mapping = mapping_menu[mapping_choice]
    tab1, tab2, tab3 = st.tabs(["Pulso", "Sinal", "PSD"])
    with tab1:
        t = np.linspace(-4, 4, 1000)
        pt = pulse.waveform(t)
        f = np.linspace(-4, 4, 1000)
        pf = pulse.spectrum(f)
        fig, ax = plt.subplots(1,2)
        ax[0].plot(t, pt, 'C0')
        ax[0].set_ylim(-1.2, 1.2)
        ax[0].set_xlabel("$f$")
        ax[0].set_ylabel("$P(f)$")
        ax[0].grid()
        ax[1].plot(f, np.abs(pf), 'C1')
        ax[1].set_xlabel("$f$")
        ax[1].set_ylabel("$|P(f)|$")
        ax[1].grid()
        fig.tight_layout()
        fig.set_figheight(4)
        st.pyplot(fig)
    with tab2:
        sps = 100
        pam = komm.TransmitFilter(pulse, sps)
        bn = [[1, 0, 0, 1, 1, 1, 0, 1, 0, 1]]
        st.write(f"Bits: {bn}")
        xn = mapping(bn)
        yt = pam(xn)
        t = pam.time(xn)
        fig, ax = plt.subplots(2,1)
        ax[0].stem(xn)
        ax[0].set_xlabel("$n$")
        ax[0].set_ylabel("$x[n]$")
        ax[0].grid()
        ax[0].set_ylim([-1.1, 1.1])
        ax[1].plot(t, yt)     
        ax[1].set_xlabel("$t$")
        ax[1].set_ylabel("$y(t)$")
        ax[1].grid()
        ax[1].set_ylim([-1.1, 1.1])
        fig.tight_layout()
        st.pyplot(fig)
    with tab3:
  
        Rb = 1 / Tb
        sps = 100 #samples per symbol = samples/bit
        fa = sps*1.0 # Nyquist frequency
        n_bits = 50
        Na_bits = n_bits * sps # number of samples
        dur = n
        f = np.arange(-Na_bits//2, Na_bits//2) / Na_bits * fa # Eixo das frequencias
        yts = []
        for _ in range(1, 1000):
            bn = np.random.randint(0, 2, n_bits)
            xn = mapping(bn)
            yt = pam(xn)
            yts.append(yt)    
        yfs = fftshift(fft(yts)) / sps
        psd_sim = np.mean.abs((yfs)**2, axis=0)
        psd_teo = A**2 * Tb * np.sinc(f*Tb)**2
        fig, ax = plt.subplots()
        ax.plot(f, psd_sim, label="Simulado")
        ax.plot(f, psd_teo, label="Teórico")
        ax.set_xlim(-4, 4)
        ax.set_ylim(-0.05, 0.1)
        ax.legend()
        ax.grid()
        st.pyplot(fig)     

if __name__ == "__main__":
    main()
