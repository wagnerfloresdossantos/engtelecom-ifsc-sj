import komm.abc
import numpy as np
import matplotlib.pylab as plt
import streamlit as st
import komm
import komm.abc



def main():
    pulse_menu = {
        "Retangula NRZ": komm.RectangularPulse(1),
        "Retangular RZ": komm.RectangularPulse(0.5),
        "Manchester": komm.ManchesterPulse(),
        "Sinc": komm.SincPulse(),
    }

    st.title("PAM")
    pulse_choice = st.segmented_control(
        labbel = "Pulso",
        options=pulse_menu.keys(),
        default="Retangular NRZ",
    )
    if pulse_choice is None:
        raise Exception("Selecione um pulso")
    pulse : komm.abc.Pulse = pulse_menu[pulse_choice]
    
    tab1, tab2 = st.tabs(["Pulso", "Sinal"])

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
        xn = [0.4, 0.0, -0.2, 1.0, -1.0, -0.5]
        yt = pam(xn)
        t = pam.time(xn)
        fig, ax = plt.subplots(2,1)
        ax[0].stem(xn)
        ax[0].set_xlabel("$n$")
        ax[0].set_ylabel("$x[n]$")
        ax[0].grid()
        ax[0].set_xlim([-1, 7])

        ax[1].plot(t, yt)
        ax[1].plot(xn, linestyle='None', marker='o')
        ax[1].set_xlabel("$t$")
        ax[1].set_ylabel("$y(t)$")
        ax[1].grid()
        ax[1].set_ylim([-1, 7])
        fig.tight_layout()
        st.pyplot(fig)

                   
    if __name__ == "__main__":
        main()