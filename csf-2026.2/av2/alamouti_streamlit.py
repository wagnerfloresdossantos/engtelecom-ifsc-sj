"""
Demonstração interativa de diversidade espacial com o código de Alamouti.

Execute:
    python3 -m pip install streamlit numpy pandas plotly
    streamlit run alamouti_streamlit.py
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Código de Alamouti",
    page_icon="📡",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
    [data-testid="stMetricValue"] {font-size: 1.35rem;}
    @media (min-width: 1100px) {
        .block-container {max-width: 1250px;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def fmt_complex(z: complex, precision: int = 3) -> str:
    """Formata um número complexo sem produzir '+ -'."""
    sign = "+" if z.imag >= 0 else "−"
    return f"{z.real:.{precision}f} {sign} j{abs(z.imag):.{precision}f}"


def bpsk(bit):
    """Mapeamento 0 -> +1 e 1 -> -1."""
    return 1.0 - 2.0 * np.asarray(bit)


def complex_noise(rng, size, n0):
    """Ruído AWGN complexo circular com potência média N0."""
    return np.sqrt(n0 / 2.0) * (
        rng.standard_normal(size) + 1j * rng.standard_normal(size)
    )


def rayleigh_channel(rng, size):
    """Canal Rayleigh complexo normalizado: E[|h|²] = 1."""
    return (
        rng.standard_normal(size) + 1j * rng.standard_normal(size)
    ) / np.sqrt(2.0)


def one_alamouti_example(bit1, bit2, h1, h2, ebn0_db, seed):
    """Executa um bloco Alamouti 2x1 com potência total normalizada."""
    rng = np.random.default_rng(seed)
    s1, s2 = float(bpsk(bit1)), float(bpsk(bit2))
    scale = 1.0 / np.sqrt(2.0)
    n0 = 10.0 ** (-ebn0_db / 10.0)
    n1, n2 = complex_noise(rng, 2, n0)

    # Intervalo 1: [s1, s2]; intervalo 2: [-s2*, s1*].
    y1 = scale * (h1 * s1 + h2 * s2) + n1
    y2 = scale * (-h1 * np.conj(s2) + h2 * np.conj(s1)) + n2

    # Combinador ortogonal de Alamouti.
    z1 = np.conj(h1) * y1 + h2 * np.conj(y2)
    z2 = np.conj(h2) * y1 - h1 * np.conj(y2)
    gain = scale * (abs(h1) ** 2 + abs(h2) ** 2)
    s1_hat = z1 / gain
    s2_hat = z2 / gain
    bit1_hat = int(np.real(s1_hat) < 0)
    bit2_hat = int(np.real(s2_hat) < 0)

    return {
        "s1": s1,
        "s2": s2,
        "n1": n1,
        "n2": n2,
        "y1": y1,
        "y2": y2,
        "z1": z1,
        "z2": z2,
        "s1_hat": s1_hat,
        "s2_hat": s2_hat,
        "bit1_hat": bit1_hat,
        "bit2_hat": bit2_hat,
        "gain": gain,
    }


@st.cache_data(show_spinner=False)
def simulate_ber(ebn0_values, n_bits, seed):
    """Compara BPSK SISO 1x1 e Alamouti 2x1 em canal Rayleigh."""
    rng = np.random.default_rng(seed)
    n_bits = int(n_bits)
    if n_bits % 2:
        n_bits += 1

    bits = rng.integers(0, 2, n_bits)
    symbols = bpsk(bits)
    ber_siso, ber_alamouti = [], []
    scale = 1.0 / np.sqrt(2.0)

    for ebn0_db in ebn0_values:
        n0 = 10.0 ** (-float(ebn0_db) / 10.0)

        # SISO: detecção coerente com conhecimento perfeito do canal.
        h = rayleigh_channel(rng, n_bits)
        y = h * symbols + complex_noise(rng, n_bits, n0)
        detected = (np.real(np.conj(h) * y) < 0).astype(int)
        ber_siso.append(np.mean(detected != bits))

        # Alamouti 2x1: dois bits transmitidos em dois intervalos.
        b1, b2 = bits[0::2], bits[1::2]
        s1, s2 = bpsk(b1), bpsk(b2)
        blocks = len(s1)
        h1 = rayleigh_channel(rng, blocks)
        h2 = rayleigh_channel(rng, blocks)
        y1 = scale * (h1 * s1 + h2 * s2) + complex_noise(rng, blocks, n0)
        y2 = scale * (-h1 * s2 + h2 * s1) + complex_noise(rng, blocks, n0)

        z1 = np.conj(h1) * y1 + h2 * np.conj(y2)
        z2 = np.conj(h2) * y1 - h1 * np.conj(y2)
        detected_1 = (np.real(z1) < 0).astype(int)
        detected_2 = (np.real(z2) < 0).astype(int)
        errors = np.count_nonzero(detected_1 != b1)
        errors += np.count_nonzero(detected_2 != b2)
        ber_alamouti.append(errors / n_bits)

    return np.asarray(ber_siso), np.asarray(ber_alamouti)


def constellation_figure(points, labels, title):
    fig = go.Figure()
    colors = ["#1565c0", "#e65100"]
    for point, label, color in zip(points, labels, colors):
        fig.add_trace(
            go.Scatter(
                x=[np.real(point)],
                y=[np.imag(point)],
                mode="markers+text",
                marker={"size": 15, "color": color},
                text=[label],
                textposition="top center",
                name=label,
            )
        )
    fig.add_vline(x=0, line_dash="dot", line_color="gray")
    fig.add_hline(y=0, line_dash="dot", line_color="gray")
    fig.update_layout(
        title=title,
        xaxis_title="Componente em fase (I)",
        yaxis_title="Componente em quadratura (Q)",
        height=390,
        showlegend=False,
    )
    return fig


st.title("📡 Diversidade espacial e código de Alamouti")
st.caption(
    "Seminário interativo — sistema STBC 2×1 em canal Rayleigh com modulação BPSK"
)

with st.sidebar:
    st.header("Seminário")
    st.markdown(
        """
        **Instituto Federal de Santa Catarina**  
        Campus São José

        **Disciplina:** Comunicações sem Fio  
        **Professor:** Evanaska Maria Barbosa Nogueira  
        **Aluno:** Wagner Flores dos Santos  
        **Curso:** Engenharia de Telecomunicações  
        **Semestre:** 2026.2
        """
    )
    st.divider()
    st.markdown(
        """
        **Ordem sugerida**

        1. Capa e objetivo
        2. Fundamentação
        3. Transmissão passo a passo
        4. Curvas de BER
        5. Síntese e conclusão
        6. Operação e referências
        """
    )
    st.caption("Dica: pressione F11 para apresentar em tela cheia.")

with st.expander("Objetivo e hipóteses da demonstração"):
    st.markdown(
        """
        O código de Alamouti transmite dois símbolos por duas antenas durante dois
        intervalos. O receptor combina duas cópias independentes de cada símbolo,
        reduzindo a probabilidade de um desvanecimento profundo.

        **Hipóteses:** canal aproximadamente constante durante os dois intervalos,
        estimação perfeita de $h_1$ e $h_2$, ruído AWGN e potência total
        igual à do sistema SISO. O fator $1/\\sqrt{2}$ divide a potência entre
        as duas antenas.
        """
    )

tab0, tab_theory, tab1, tab2, tab3, tab_guide, tab_refs = st.tabs(
    [
        "Capa",
        "Fundamentação",
        "Demonstração",
        "BER",
        "Conclusão",
        "Como operar",
        "Referências",
    ]
)

with tab0:
    st.markdown("## Diversidade espacial em sistemas de comunicação sem fio")
    st.markdown("### O código espaço-temporal de Alamouti")
    st.write("")
    left, right = st.columns([3, 2])
    with left:
        st.markdown(
            """
            **Instituto Federal de Santa Catarina — Campus São José**

            **Disciplina:** Comunicações sem Fio  
            **Professor:** Evanaska Maria Barbosa Nogueira  
            **Aluno:** Wagner Flores dos Santos  
            **Curso:** Engenharia de Telecomunicações  
            **Semestre:** 2026.2
            """
        )
    with right:
        st.info(
            "**Pergunta norteadora**\n\nComo duas antenas transmissoras podem "
            "reduzir os efeitos do desvanecimento sem aumentar a largura de banda?"
        )

    st.divider()
    st.markdown("#### Objetivo")
    st.markdown(
        """
        Explicar o princípio da **diversidade espacial**, apresentar o código de
        Alamouti para duas antenas transmissoras e uma receptora e demonstrar,
        por simulação, sua vantagem sobre um enlace SISO em canal Rayleigh.
        """
    )
    a, b, c = st.columns(3)
    a.metric("Antenas", "2 Tx × 1 Rx")
    b.metric("Taxa do código", "1 símbolo/uso")
    c.metric("Ordem de diversidade", "2")
    st.success(
        "Ideia central: a informação percorre dois canais independentes. "
        "Se um estiver em desvanecimento profundo, o outro ainda poderá preservá-la."
    )

with tab_theory:
    st.subheader("1. O canal sem fio e o desvanecimento")
    st.markdown(
        r"""
        Em um ambiente real, o sinal chega ao receptor por vários caminhos devido
        a **reflexões, difrações e espalhamento**. As cópias possuem amplitudes,
        fases e atrasos diferentes. Sua soma pode ser construtiva ou destrutiva,
        produzindo variações rápidas da potência recebida: o **desvanecimento em
        pequena escala**.

        Quando não existe uma componente de visada dominante, a envoltória do
        canal é frequentemente modelada pela distribuição de **Rayleigh**. Neste
        aplicativo, cada enlace é representado por
        $$
        h_i \sim \mathcal{CN}(0,1), \qquad E[|h_i|^2]=1.
        $$
        """
    )

    st.subheader("2. O princípio da diversidade")
    st.markdown(
        """
        Diversidade significa fornecer ao receptor versões da mesma informação
        afetadas por desvanecimentos pouco correlacionados. As formas mais comuns são:
        """
    )
    diversity_table = pd.DataFrame(
        {
            "Tipo": ["Temporal", "Em frequência", "Espacial"],
            "Como funciona": [
                "Repete ou codifica a informação em instantes diferentes",
                "Usa frequências ou subportadoras distintas",
                "Usa antenas separadas no transmissor e/ou receptor",
            ],
            "Recurso necessário": [
                "Tempo e canal variável",
                "Largura de banda",
                "Múltiplas antenas",
            ],
        }
    )
    st.table(diversity_table)
    st.markdown(
        "No Alamouti, a diversidade é obtida no **transmissor**, o que é útil "
        "quando o terminal receptor possui apenas uma antena."
    )

    st.subheader("3. O código de Alamouti")
    st.markdown(
        r"""
        Dois símbolos complexos, $s_1$ e $s_2$, são enviados por duas antenas
        durante dois intervalos. A potência total é normalizada por
        $1/\sqrt{2}$:
        $$
        \mathbf{S}=\frac{1}{\sqrt{2}}
        \begin{bmatrix}
        s_1 & s_2\\
        -s_2^* & s_1^*
        \end{bmatrix}.
        $$
        A primeira linha corresponde ao primeiro intervalo e a segunda ao segundo.
        As colunas representam as antenas 1 e 2. O conjugado e a troca de sinais
        criam uma estrutura **ortogonal**.
        """
    )

    st.subheader("4. Recepção e combinação")
    st.markdown(
        r"""
        Considerando canais $h_1$ e $h_2$ constantes durante o bloco:
        $$
        y_1=\frac{h_1s_1+h_2s_2}{\sqrt{2}}+n_1,
        \qquad
        y_2=\frac{-h_1s_2^*+h_2s_1^*}{\sqrt{2}}+n_2.
        $$
        O receptor calcula
        $$
        \tilde{s}_1=h_1^*y_1+h_2y_2^*, \qquad
        \tilde{s}_2=h_2^*y_1-h_1y_2^*.
        $$
        Os termos de interferência entre $s_1$ e $s_2$ se cancelam. Cada
        estimativa passa a depender do ganho combinado
        $|h_1|^2+|h_2|^2$. Portanto, os dois canais precisariam estar fracos
        simultaneamente para causar um desvanecimento profundo.
        """
    )

    st.subheader("5. O que o Alamouti oferece — e o que não oferece")
    pros, limits = st.columns(2)
    with pros:
        st.success(
            "**Vantagens**\n\n"
            "• diversidade de ordem 2;\n\n"
            "• taxa unitária;\n\n"
            "• decodificação linear simples;\n\n"
            "• não exige conhecer o canal no transmissor."
        )
    with limits:
        st.warning(
            "**Hipóteses e limitações**\n\n"
            "• receptor precisa estimar os canais;\n\n"
            "• canal deve variar pouco em dois intervalos;\n\n"
            "• requer duas cadeias de transmissão;\n\n"
            "• melhora confiabilidade, não duplica a taxa."
        )

with tab1:
    st.subheader("Um bloco de transmissão")
    controls, explanation = st.columns([1, 2])

    with controls:
        bit1 = st.selectbox("Primeiro bit, b₁", [0, 1], index=0)
        bit2 = st.selectbox("Segundo bit, b₂", [0, 1], index=1)
        ebn0_single = st.slider("Eᵦ/N₀ (dB)", -5, 25, 8)
        channel_mode = st.radio(
            "Coeficientes do canal",
            ["Gerados automaticamente", "Definidos manualmente"],
        )
        seed_single = st.number_input(
            "Semente aleatória", min_value=0, value=42, step=1
        )

        if channel_mode == "Gerados automaticamente":
            channel_rng = np.random.default_rng(int(seed_single))
            h1, h2 = rayleigh_channel(channel_rng, 2)
        else:
            st.markdown("**Canal da antena 1**")
            h1r = st.number_input("Re{h₁}", value=0.80, step=0.05)
            h1i = st.number_input("Im{h₁}", value=0.30, step=0.05)
            st.markdown("**Canal da antena 2**")
            h2r = st.number_input("Re{h₂}", value=-0.25, step=0.05)
            h2i = st.number_input("Im{h₂}", value=0.65, step=0.05)
            h1, h2 = complex(h1r, h1i), complex(h2r, h2i)

        result = one_alamouti_example(
            bit1, bit2, h1, h2, ebn0_single, int(seed_single) + 1000
        )

    with explanation:
        st.markdown(
            r"""
            Para símbolos $s_1$ e $s_2$, a matriz espaço-temporal é:
            $$
            \mathbf{S}=\frac{1}{\sqrt{2}}
            \begin{bmatrix}
            s_1 & s_2\\
            -s_2^* & s_1^*
            \end{bmatrix}.
            $$
            As **linhas** representam os intervalos e as **colunas**, as antenas.
            """
        )

        tx_table = pd.DataFrame(
            {
                "Intervalo": ["t₁", "t₂"],
                "Antena 1": [
                    f"s₁ = {result['s1']:+.0f}",
                    f"−s₂* = {-result['s2']:+.0f}",
                ],
                "Antena 2": [
                    f"s₂ = {result['s2']:+.0f}",
                    f"s₁* = {result['s1']:+.0f}",
                ],
            }
        )
        st.table(tx_table)

        c1, c2, c3 = st.columns(3)
        c1.metric("h₁", fmt_complex(h1))
        c2.metric("h₂", fmt_complex(h2))
        c3.metric("Ganho combinado", f"{abs(h1)**2 + abs(h2)**2:.3f}")

    st.divider()
    received, detected = st.columns(2)
    with received:
        st.markdown("#### Sinais recebidos")
        st.latex(
            r"y_1=\frac{h_1s_1+h_2s_2}{\sqrt{2}}+n_1"
        )
        st.latex(
            r"y_2=\frac{-h_1s_2^*+h_2s_1^*}{\sqrt{2}}+n_2"
        )
        st.write(f"**y₁ =** {fmt_complex(result['y1'])}")
        st.write(f"**y₂ =** {fmt_complex(result['y2'])}")

    with detected:
        st.markdown("#### Combinação e decisão")
        st.latex(r"\tilde{s}_1=h_1^*y_1+h_2y_2^*")
        st.latex(r"\tilde{s}_2=h_2^*y_1-h_1y_2^*")
        st.write(f"**Estimativa de s₁:** {fmt_complex(result['s1_hat'])}")
        st.write(f"**Estimativa de s₂:** {fmt_complex(result['s2_hat'])}")

        ok1 = result["bit1_hat"] == bit1
        ok2 = result["bit2_hat"] == bit2
        st.write(
            f"Bit 1 detectado: **{result['bit1_hat']}** "
            f"{'✅' if ok1 else '❌'}"
        )
        st.write(
            f"Bit 2 detectado: **{result['bit2_hat']}** "
            f"{'✅' if ok2 else '❌'}"
        )

    st.plotly_chart(
        constellation_figure(
            [result["s1_hat"], result["s2_hat"]],
            ["ŝ₁", "ŝ₂"],
            "Estimativas após a combinação de Alamouti",
        ),
        use_container_width=True,
    )

with tab2:
    st.subheader("Comparação Monte Carlo")
    st.markdown(
        """
        Cada ponto é obtido transmitindo bits por canais Rayleigh independentes.
        Uma BER menor significa uma comunicação mais confiável. As duas técnicas
        utilizam a **mesma energia total por bit**.
        """
    )

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        n_bits = st.select_slider(
            "Bits por ponto",
            options=[10_000, 20_000, 50_000, 100_000, 200_000],
            value=50_000,
        )
    with col_b:
        max_snr = st.slider("Eᵦ/N₀ máximo (dB)", 10, 30, 24, step=2)
    with col_c:
        seed_ber = st.number_input(
            "Semente da simulação", min_value=0, value=2026, step=1
        )

    ebn0_values = np.arange(0, max_snr + 1, 2, dtype=float)
    with st.spinner("Simulando transmissões..."):
        ber_siso, ber_alamouti = simulate_ber(
            tuple(ebn0_values), int(n_bits), int(seed_ber)
        )

    # Evita zero em escala log; o marcador indica o limite observável.
    plot_floor = 0.5 / n_bits
    siso_plot = np.maximum(ber_siso, plot_floor)
    alamouti_plot = np.maximum(ber_alamouti, plot_floor)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=ebn0_values,
            y=siso_plot,
            mode="lines+markers",
            name="SISO 1×1",
            line={"width": 3, "color": "#e65100"},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=ebn0_values,
            y=alamouti_plot,
            mode="lines+markers",
            name="Alamouti 2×1",
            line={"width": 3, "color": "#1565c0"},
        )
    )
    fig.update_layout(
        title="BER da BPSK em canal Rayleigh",
        xaxis_title="Eᵦ/N₀ (dB)",
        yaxis_title="Taxa de erro de bit (BER)",
        yaxis_type="log",
        yaxis_range=[np.log10(plot_floor) - 0.2, 0],
        height=520,
        hovermode="x unified",
        legend={"orientation": "h", "y": 1.1},
    )
    st.plotly_chart(fig, use_container_width=True)

    results_df = pd.DataFrame(
        {
            "Eᵦ/N₀ (dB)": ebn0_values.astype(int),
            "BER SISO 1×1": ber_siso,
            "BER Alamouti 2×1": ber_alamouti,
        }
    )
    st.dataframe(
        results_df.style.format(
            {"BER SISO 1×1": "{:.3e}", "BER Alamouti 2×1": "{:.3e}"}
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.info(
        "Quando não ocorre nenhum erro, o gráfico usa 0,5/N como limite "
        "visual da simulação. Aumente o número de bits para observar BERs menores."
    )

with tab3:
    st.subheader("Síntese e conclusão")
    st.markdown(
        r"""
        1. **O problema:** no multipercurso, uma cópia do sinal pode sofrer
           desvanecimento profundo.
        2. **A ideia da diversidade:** criar cópias independentes da informação.
        3. **O Alamouti:** transmite dois símbolos por duas antenas em dois
           intervalos, mantendo taxa unitária.
        4. **A ortogonalidade:** permite separar $s_1$ e $s_2$ com
           um combinador linear simples.
        5. **O resultado:** a qualidade depende da soma
           $|h_1|^2+|h_2|^2$. É improvável que os dois canais estejam em
           desvanecimento profundo simultaneamente.
        6. **O preço:** duas antenas transmissoras, conhecimento do canal no
           receptor e canal quase constante durante o bloco.
        """
    )

    st.success(
        "O código de Alamouti não tem como objetivo duplicar a velocidade. Ele usa as antenas para aumentar a **confiabilidade** do enlace. "
    )

    st.info(
        "O código de Alamouti explora duas antenas transmissoras para criar duas "
        "cópias independentes de cada símbolo. Sua estrutura ortogonal permite "
        "separá-las com baixa complexidade. Em canal Rayleigh, isso reduz "
        "significativamente a probabilidade de erro, principalmente em valores "
        "mais altos de Eᵦ/N₀. O ganho obtido é de confiabilidade, e não de "
        "velocidade: dois símbolos são enviados em dois intervalos."
    )


    st.markdown("#### Metodologia da simulação")
    st.markdown(
        r"""
        A BER é estimada por Monte Carlo. Bits equiprováveis são modulados em
        BPSK, transmitidos por canais Rayleigh planos e contaminados por AWGN.
        O receptor possui conhecimento perfeito do canal. SISO e Alamouti usam
        a mesma energia total por bit; no sistema 2×1, a amplitude de cada antena
        é multiplicada por $1/\sqrt{2}$. Esse cuidado evita atribuir à
        diversidade um ganho causado apenas por potência adicional.
        """
    )

    st.warning(
        "Os resultados são estimativas estatísticas. Com poucos bits, podem "
        "ocorrer pequenas variações entre execuções, principalmente em BER baixa."
    )

with tab_guide:
    st.subheader("Como operar durante o seminário")
    st.markdown(
        """
        Use o aplicativo como uma sequência de slides. Cada aba corresponde a uma
        etapa da apresentação. O roteiro abaixo foi pensado para aproximadamente
        **12 a 15 minutos**, podendo ser reduzido.
        """
    )

    guide = pd.DataFrame(
        {
            "Etapa": [
                "1. Capa",
                "2. Fundamentação",
                "3. Demonstração",
                "4. BER",
                "5. Conclusão",
            ],
            "Tempo": ["1 min", "4–5 min", "3–4 min", "2–3 min", "1 min"],
            "Ação": [
                "Apresente a pergunta norteadora e o objetivo",
                "Explique multipercurso, diversidade e a matriz de Alamouti",
                "Escolha dois bits, mostre os dois intervalos e a decisão",
                "Compare as curvas SISO e 2×1, variando Eᵦ/N₀",
                "Retome a confiabilidade, a taxa unitária e as limitações",
            ],
        }
    )
    st.table(guide)

    st.markdown("#### Demonstração recomendada")
    st.markdown(
        """
        1. Abra **Demonstração** e mantenha inicialmente os bits `0` e `1`.
        2. Use canais gerados automaticamente e comece com **Eᵦ/N₀ = 8 dB**.
        3. Mostre que cada símbolo é transmitido pelas duas antenas em momentos diferentes.
        4. Aponte os valores de `h₁`, `h₂` e o ganho combinado.
        5. Explique as duas equações de combinação e os bits recuperados.
        6. Mude a semente para mostrar outro canal e repita rapidamente.
        7. Abra **BER**, use 50.000 ou 100.000 bits e compare as duas curvas.
        8. Destaque que a separação entre as curvas cresce com Eᵦ/N₀.
        """
    )

    st.markdown("#### Preparação antes da aula")
    st.markdown(
        """
        - Ative o ambiente virtual e abra o aplicativo antes de conectar ao projetor.
        - Pressione **F11** para usar o navegador em tela cheia.
        - Faça uma simulação de BER antecipadamente para aquecer o cache.
        - Use 50.000 bits durante a apresentação para obter resposta rápida.
        - Se houver tempo, aumente para 200.000 bits e explique a precisão estatística.
        - Não dependa da internet: depois de instaladas, as bibliotecas rodam localmente.
        """
    )

    st.markdown("#### Comandos para iniciar")
    st.code(
        "source .venv/bin/activate\n"
        "python -m streamlit run alamouti_streamlit.py",
        language="bash",
    )
    st.caption("Para encerrar, pressione Ctrl+C no terminal.")

with tab_refs:
    st.subheader("Referências")
    st.markdown(
        """
        **Referência principal**

        ALAMOUTI, Siavash M. A simple transmit diversity technique for wireless
        communications. *IEEE Journal on Selected Areas in Communications*,
        v. 16, n. 8, p. 1451–1458, out. 1998.  
        DOI: [10.1109/49.730453](https://doi.org/10.1109/49.730453)

        **Referências complementares**

        GOLDSMITH, Andrea. *Wireless Communications*. Cambridge: Cambridge
        University Press, 2005.

        TSE, David; VISWANATH, Pramod. *Fundamentals of Wireless Communication*.
        Cambridge: Cambridge University Press, 2005.

        **Material da disciplina**

        NOGUEIRA, Evanaska Maria Barbosa. *Comunicações sem fio: diversidade,
        MIMO, OFDM, Alamouti e beamforming*. Material de aula. IFSC — Campus
        São José, 2026.
        """
    )


st.divider()
st.caption(
    "IFSC — Campus São José | Comunicações sem Fio | Wagner Flores dos Santos | 2026.2"
)
