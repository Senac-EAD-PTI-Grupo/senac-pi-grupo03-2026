import streamlit as st
import pandas as pd
from pathlib import Path

# Buscando a base tratada na pasta oficial do grupo
DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "base_tratada.csv"

st.set_page_config(page_title="Entrega de Análise Visual — Julio", layout="wide")

# Carregar os dados de forma segura
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    st.error(f"Arquivo não encontrado em: {DATA_FILE}. Certifique-se de que a base tratada existe na pasta data.")
    st.stop()

st.title("Entrega Técnica: Análise Visual & Design BI")
st.caption("Desenvolvido por: Julio Valença | Resposta às Questões de Negócio")

# ==============================================================================
# DEMANDA 1: ANÁLISE VISUAL (Saúde Mental e Desempenho)
# ==============================================================================
st.header("1. Análise Visual — Gráficos de Correlação e Distribuição")

# Questão: Média do CGPA dos alunos com nível de estresse acima de 6
estresse_alto = df[df["Stress_Index"] > 6]
cgpa_medio_estresse = estresse_alto["CGPA"].mean()

# Questão: Diferença no nível de estresse entre quem trabalha e quem não trabalha
estresse_trabalha = df.groupby("Part_Time_Job")["Stress_Index"].mean().reset_index()

col1, col2 = st.columns(2)

with col1:
    st.metric("Média de CGPA (Alunos com Estresse > 6)", f"{cgpa_medio_estresse:.2f}")
    st.markdown("**Distribuição de Notas (CGPA) por Nível de Estresse:**")
    st.scatter_chart(data=df, x="Stress_Index", y="CGPA", color="Dropout")

with col2:
    st.markdown("**Média de Estresse: Trabalha Meio Período (1) vs Não Trabalha (0):**")
    st.bar_chart(data=estresse_trabalha.set_index("Part_Time_Job")["Stress_Index"])

st.divider()

# ==============================================================================
# DEMANDA 2: DESIGN BI (Idade e Evasão)
# ==============================================================================
st.header("2. Design BI — Painel Avançado de Idades")

# Questão: Quais são as 10 idades com maior taxa de evasão?
top_10_idades = (
    df.groupby("Age")["Dropout"]
    .mean()
    .reset_index()
    .sort_values(by="Dropout", ascending=False)
    .head(10)
)
top_10_idades["Taxa_Evasao_%"] = (top_10_idades["Dropout"] * 100).round(1)

st.markdown("**Top 10 Idades com Maior Taxa Proporcional de Evasão:**")

# Exibe a tabela utilizando a largura atualizada 'stretch' exigida em 2026
st.dataframe(
    top_10_idades[["Age", "Taxa_Evasao_%"]],
    width='stretch',
    hide_index=True
)

st.bar_chart(data=top_10_idades.set_index("Age")["Taxa_Evasao_%"])
