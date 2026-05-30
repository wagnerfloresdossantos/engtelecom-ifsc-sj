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

seed = st.sidebar.number_input(
    "Semente PRNG",
    min_value=0,
    max_value=999999,
    value=42,
    step=1
)


# ==========================================
# SIMULADOR INTERATIVO
# ==========================================

st.divider()

st.header("🧪 Simulador Interativo")

st.info(
    """
    Esta seção utiliza os valores definidos nos sliders da barra lateral.

    Use esta parte para testar diferentes valores de λ, µ, k e tempo de simulação.
    """
)

if st.button("Executar Simulação com os Sliders"):

    sim = Simulator(
        end_time=simulation_time,
        lambda_rate=lambda_rate,
        mu=mu,
        k=k,
        seed=seed
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
    )

    # ======================================
    # MÉTRICAS
    # ======================================

    st.subheader("📊 Resultados da Simulação Interativa")

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

            "λ utilizado",
            "µ utilizado",
            "k utilizado",
            "Semente PRNG",
            "Carga oferecida A",
            "Bloqueio Simulado",
            "Bloqueio Teórico",
            "Erro Absoluto",
            "Utilização",
            "Vazão"

        ],

        "Valor": [

            f"{lambda_rate:.2f}",
            f"{mu:.2f}",
            f"{k}",
            f"{seed}",
            f"{A:.4f}",
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

    st.subheader("📈 Comparação Teórico vs Simulado")

    comparison_df = pd.DataFrame({

        "Tipo": [
            "Teórico",
            "Simulado"
        ],

        "Probabilidade de Bloqueio": [
            theoretical,
            simulated
        ]

    })

    fig_compare = px.bar(

        comparison_df,

        x="Tipo",

        y="Probabilidade de Bloqueio",

        color="Tipo",

        text="Probabilidade de Bloqueio",

        title="Comparação Erlang-B vs DES"

    )

    fig_compare.update_traces(
        texttemplate="%{text:.6f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig_compare,
        width="stretch"
    )


# ==========================================
# EXPERIMENTOS DO ENUNCIADO
# ==========================================

st.divider()

st.header("📚 Experimentos do Enunciado")

st.info(
    """
    Esta seção executa automaticamente os cenários exigidos no enunciado:

    - λ = 2, 4, 5, 6, 8 chamadas/min
    - µ = 1 chamada/min
    - k = 9 canais

    Os sliders não alteram λ, µ e k nesta seção.
    O tempo de simulação usado continua sendo o valor definido no campo lateral.
    """
)

if st.button("Executar Experimentos do Enunciado"):

    lambdas = [2, 4, 5, 6, 8]

    experiment_results = []

    for l in lambdas:

        fixed_mu = 1
        fixed_k = 9

    
        sim = Simulator(
            end_time=simulation_time,
            lambda_rate=l,
            mu=fixed_mu,
            k=fixed_k,
            seed=seed + l
        )
        sim.run()

        results = sim.results()

        A = l / fixed_mu

        theoretical = erlang_b(
            fixed_k,
            A
        )

        simulated = results[
            "blocking_probability"
        ]

        error = abs(
            simulated - theoretical
        ) 

        experiment_results.append({

            "Lambda": l,

            "Mu":
                fixed_mu,

            "k":
                fixed_k,

             "Semente PRNG":
                seed + l,

            "Carga A":
                A,

            "Bloqueio Teórico":
                theoretical,

            "Bloqueio Simulado":
                simulated,

            "Erro Absoluto":
                error,

            "Utilização":
                results["utilization"],

            "Vazão":
                results["throughput"]

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
    # GRÁFICO TEORIA VS SIMULAÇÃO
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

        markers=True,

        title="Probabilidade de Bloqueio: Erlang-B vs DES"

    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # ======================================
    # GRÁFICO DO ERRO Absoluto
    # ======================================

    st.subheader(
        "📉 Erro Absoluto"
    )

    fig_error = px.bar(

        df,

        x="Lambda",

        y="Erro Absoluto",

        text="Erro Absoluto",

        title="Erro Absoluto entre Teoria e Simulação"

    )

    fig_error.update_traces(
        texttemplate="%{text:.4f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig_error,
        width="stretch"
    )