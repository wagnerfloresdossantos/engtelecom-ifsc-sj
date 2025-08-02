import numpy as np
import streamlit as st
import komm
import matplotlib.pyplot as plt

st.title("Diagrama de Olho")

rolloff = st.slider(
    label="Rolloff $\\alpha$",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01,
)

pulse = komm.RaisedCosinePulse(rolloff)
tabs = st.tabs(["pulso", "Sinal", "olho"])

with tabs[0]:
    fig, ax = plt.subplots(1, 2, figsize=(12,4))
    ts = np.linspace(-8, 8, num=1000)
    ax[0].plot(ts, pulse.waveform(ts))
    ax[0].set_ylim(-0.25, 1.25)
    ax[0].grid()
    ax[0].set_xlabel("Tempo")
    ax[0].set_ylabel("Amplitude")
    fs = np.linspace(-8, 8, num=1000)
    ax[1].plot(fs, np.real(pulse.spectrum(fs)))
    ax[1].set_ylim(-0.25, 1.25)
    ax[1].grid()
    ax[1].set_xlabel("$f$ (Hz)")
    ax[1].set_ylabel("$p(f)$")
    st.pyplot(fig)
    st.pyplot(fig)
with tabs[1]:
    sps = 20
    rng = np.random.default_rng(seed=7)
    source = komm.DiscreteMemorylessSource([0.5, 0.5])
    bits = source(1000)
    x = 2.0*bits - 1.0
    tx_filter = komm.TransmitFilter(pulse, sps)
    y = tx_filter(x)
    ts, _ = tx_filter.axes(x)
    ns = np.arange(31)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(ts, y)
    ax.plot(ns, x[:31], "o")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("$y(t)$")
    ax.set_ylim(-2.5, 2.5)
    ax.set_xlim(-10, 30)
    ax.grid()
    st.pyplot(fig)

with tabs[2]:
    fig, ax = plt.subplots(figsize=(6, 3))
    span = 3
    samples_per_span = span * sps
    for i in range(bits.size // span):
        ts = np.linspace(0, span, num=samples_per_span+1)
    ax.plot(ts, y[samples_per_span*i:samples_per_span*(i+1)+1], "C0", alpha=0.25)
    ax.set_ylim(-2.5, 2.5)
    ax.grid()
    st.pyplot(fig)

