import pandas as pd
import streamlit as st
import plotly.express as px

from simulator import Simulator
from erlang import erlang_b


# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Simulador M/M/k/k",
    layout="wide"
)


# ==========================================
# TÍTULO
# ==========================================

st.title("📡 Simulador M/M/k/k")

st.write(
    """
    Simulação a Eventos Discretos (DES)
    para sistemas celulares com bloqueio
    usando Erlang-B.
    """
)

st.latex(
    r"""
    B(k,A)=
    \frac{
        \frac{A^k}{k!}
    }{
        \sum_{i=0}^{k}
        \frac{A^i}{i!}
    }
    """
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("Parâmetros")

lambda_rate = st.sidebar.slider(
    "Taxa de chegada λ",
    min_value=1.0,
    max_value=10.0,
    value=5.0,
    step=0.5
)

mu = st.sidebar.slider(
    "Taxa de serviço µ",
    min_value=0.5,
    max_value=5.0,
    value=1.0,
    step=0.5
)

k = st.sidebar.slider(
    "Número de canais k",
    min_value=1,
    max_value=20,
    value=9
)

simulation_time = st.sidebar.number_input(
    "Tempo de simulação",
    min_value=1000,
    max_value=1000000,
    value=10000,
    step=1000
)


# ==========================================
# SIMULAÇÃO INDIVIDUAL
# ==========================================

if st.button("Executar Simulação"):

    sim = Simulator(
        end_time=simulation_time,
        lambda_rate=lambda_rate,
        mu=mu,
        k=k
    )

    sim.run()

    results = sim.results()

    A = lambda_rate / mu

    theoretical = erlang_b(k, A)

    simulated = results[
        "blocking_probability"
    ]

    error = abs(
        simulated - theoretical
    ) / theoretical

    # ======================================
    # MÉTRICAS
    # ======================================

    st.header("📊 Resultados")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Chamadas Geradas",
        results["generated"]
    )

    col2.metric(
        "Chamadas Aceitas",
        results["accepted"]
    )

    col3.metric(
        "Chamadas Bloqueadas",
        results["blocked"]
    )

    st.divider()

    metrics_df = pd.DataFrame({

        "Métrica": [

            "Bloqueio Simulado",
            "Bloqueio Teórico",
            "Erro Relativo",
            "Utilização",
            "Vazão"

        ],

        "Valor": [

            f"{simulated:.6f}",
            f"{theoretical:.6f}",
            f"{error:.6f}",
            f"{results['utilization']:.4f}",
            f"{results['throughput']:.4f}"

        ]

    })

    st.table(metrics_df)

    # ======================================
    # COMPARAÇÃO
    # ======================================

    st.divider()

    st.header("📈 Comparação")

    comparison_df = pd.DataFrame({

        "Tipo": [
            "Teórico",
            "Simulado"
        ],

        "Probabilidade": [
            theoretical,
            simulated
        ]

    })

    fig_compare = px.bar(

        comparison_df,

        x="Tipo",

        y="Probabilidade",

        color="Tipo",

        title="Erlang-B vs DES"

    )

    st.plotly_chart(
        fig_compare,
        width="stretch"
    )


# ==========================================
# EXPERIMENTOS AUTOMÁTICOS
# ==========================================

st.divider()

st.header("📚 Experimentos Automáticos")

if st.button("Executar Experimentos do Enunciado"):

    lambdas = [2, 4, 5, 6, 8]

    experiment_results = []

    for l in lambdas:

        sim = Simulator(
            end_time=simulation_time,
            lambda_rate=l,
            mu=1,
            k=9
        )

        sim.run()

        results = sim.results()

        theoretical = erlang_b(
            9,
            l / 1
        )

        simulated = results[
            "blocking_probability"
        ]

        error = abs(
            simulated - theoretical
        ) / theoretical

        experiment_results.append({

            "Lambda": l,

            "Bloqueio Teórico":
                theoretical,

            "Bloqueio Simulado":
                simulated,

            "Erro Relativo":
                error,

            "Utilização":
                results["utilization"]

        })

    df = pd.DataFrame(
        experiment_results
    )

    # ======================================
    # TABELA
    # ======================================

    st.subheader("Tabela de Resultados")

    st.dataframe(df)

    # ======================================
    # DOWNLOAD CSV
    # ======================================

    csv = df.to_csv(index=False)

    st.download_button(

        label="⬇️ Download CSV",

        data=csv,

        file_name="resultados_mmkk.csv",

        mime="text/csv"

    )

    # ======================================
    # GRÁFICO
    # ======================================

    st.subheader(
        "📈 Teoria vs Simulação"
    )

    fig = px.line(

        df,

        x="Lambda",

        y=[
            "Bloqueio Teórico",
            "Bloqueio Simulado"
        ],

        markers=True

    )

    st.plotly_chart(
        fig,
        width="stretch"
    )