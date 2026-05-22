# 📡 Simulador M/M/k/k com DES e Erlang-B

Projeto desenvolvido para a disciplina de **Avaliação de Desempenho de Sistemas (ADS)** do curso de Engenharia de Telecomunicações do IFSC.

O sistema implementa uma **Simulação a Eventos Discretos (DES)** de um sistema celular do tipo **M/M/k/k**, comparando os resultados simulados com os resultados teóricos obtidos pela fórmula de **Erlang-B**.

---

# 🎯 Objetivos

O projeto simula:

- chegadas de chamadas segundo processo de Poisson;
- duração das chamadas com distribuição exponencial;
- múltiplos canais de comunicação;
- bloqueio imediato de chamadas quando todos os canais estão ocupados;
- cálculo de métricas de desempenho;
- comparação entre teoria e simulação.

---

# 🧠 Modelo M/M/k/k

Características do sistema:

| Característica | Descrição |
|---|---|
| M | Chegadas Poisson |
| M | Serviço exponencial |
| k | Número de canais |
| k | Capacidade máxima do sistema |
| Fila | Não possui |
| Bloqueio | Imediato |

---

# 📚 Fórmula de Erlang-B

A probabilidade teórica de bloqueio é dada por:

\[
B(k,A)=
\frac{
\frac{A^k}{k!}
}{
\sum_{i=0}^{k}
\frac{A^i}{i!}
}
\]

onde:

\[
A = \frac{\lambda}{\mu}
\]

---

# 🛠 Tecnologias Utilizadas

- Python 3
- Streamlit
- Plotly
- Pandas
- NumPy

---

# 📁 Estrutura do Projeto

```text
mmkk-streamlit/
│
├── app.py
├── simulator.py
├── events.py
├── erlang.py
├── metrics.py
├── experiment.py
├── plot_results.py
├── requirements.txt
├── results/
└── venv/
```
# ⚙️ Instalação
1. Clonar ou baixar o projeto
git clone <repositorio>

ou extraia o .zip.

2. Entrar na pasta do projeto
cd mmkk-streamlit
3. Criar ambiente virtual
python3 -m venv venv
4. Ativar ambiente virtual
Linux / Ubuntu
source venv/bin/activate
Windows
venv\Scripts\activate
5. Instalar dependências
pip install -r requirements.txt

## ▶️ Executando o Sistema
Executar aplicação Streamlit

```streamlit run app.py``

## 🌐 Acessando a Interface

Após executar o comando, o terminal exibirá:

Local URL: http://localhost:8501

Abra o navegador e acesse:

http://localhost:8501

## 🎛 Utilização do Sistema

## O sistema possui controles interativos para:

### Parâmetro	Descrição
λ	Taxa média de chegada

µ	Taxa média de atendimento

k	Número de canais

Tempo de Simulação	Tempo total do DES

# 📊 Funcionalidades

## ✅ Simulação individual

Executa uma simulação com os parâmetros escolhidos.

Métricas apresentadas:

chamadas geradas;

chamadas aceitas;

chamadas bloqueadas;

probabilidade de bloqueio simulada;

probabilidade teórica;

erro relativo;

utilização média;

vazão do sistema.

## ✅ Comparação Teoria × Simulação

O sistema gera gráficos comparando:

Erlang-B;

Simulação DES.

## ✅ Experimentos automáticos

Executa automaticamente os testes solicitados no enunciado:

λ = 2, 4, 5, 6, 8

k = 9

µ = 1

Gerando:

tabela automática;

gráfico comparativo;

download CSV.

# 📈 Resultados Esperados

Espera-se observar:

aumento da probabilidade de bloqueio conforme λ aumenta;

aumento da utilização dos canais;

aproximação entre resultados simulados e teóricos.

# 🧪 Exemplos de Teste
Teste 1

Parâmetro	Valor

λ	2

µ	1

k	9


Resultado esperado:

bloqueio muito baixo.

Teste 2

Parâmetro	Valor

λ	8

µ	1

k	9


Resultado esperado:

bloqueio significativamente maior.

# 📚 Conceitos Utilizados
Simulação a Eventos Discretos (DES)

Sistemas de Filas

Processo de Poisson

Distribuição Exponencial

Erlang-B

Probabilidade de Bloqueio

Utilização de Servidores

# 👨‍💻 Autores
Wagner e Gabriel

Projeto desenvolvido para a disciplina de:

Avaliação de Desempenho de Sistemas (ADS) (2026.1)

IFSC — Engenharia de Telecomunicações