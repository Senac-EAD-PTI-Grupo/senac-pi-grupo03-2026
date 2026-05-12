import streamlit as st
import pandas as pd
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "base_tratada.csv"

st.set_page_config(
    page_title="Análise de Evasão Acadêmica — Grupo 03",
    page_icon="🎓",
    layout="wide",
)

st.title("📊🎓 Análise de Evasão Acadêmica")
st.caption("Projeto Integrador — Grupo 03 | Senac EAD 2026")

@st.cache_data
def carregar_dados():
    return pd.read_csv(DATA_FILE)

df = carregar_dados()

# ── Sidebar: filtros ───────────────────────────────────────────────────────────
st.sidebar.header("Filtros")

departamentos = ["Todos"] + sorted(df["Department"].unique().tolist())
depto_selecionado = st.sidebar.selectbox("Departamento", departamentos)

idade_min, idade_max = int(df["Age"].min()), int(df["Age"].max())
faixa_idade = st.sidebar.slider("Faixa etária", idade_min, idade_max, (idade_min, idade_max))

# Aplicar filtros
df_filtrado = df.copy()
if depto_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Department"] == depto_selecionado]
df_filtrado = df_filtrado[
    (df_filtrado["Age"] >= faixa_idade[0]) & (df_filtrado["Age"] <= faixa_idade[1])
]

# ── Métricas resumo ────────────────────────────────────────────────────────────
total = len(df_filtrado)
evasao = int(df_filtrado["Dropout"].sum())
taxa = evasao / total * 100 if total > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total de Alunos", f"{total:,}")
col2.metric("Evadiram", f"{evasao:,}")
col3.metric("Taxa de Evasão", f"{taxa:.1f}%")

st.divider()

# ── Gráfico: taxa de evasão por departamento (entrega de Integração) ───────────
st.subheader("Taxa de Evasão por Departamento")

taxa_por_depto = (
    df_filtrado.groupby("Department")["Dropout"]
    .agg(["sum", "count"])
    .rename(columns={"sum": "Evadiram", "count": "Total"})
    .assign(Taxa=lambda x: (x["Evadiram"] / x["Total"] * 100).round(1))
    .sort_values("Taxa", ascending=False)
    .reset_index()
)

st.bar_chart(taxa_por_depto.set_index("Department")["Taxa"])

st.divider()

# ── Espaço reservado para equipe de Análise Visual (Cauã, Diego, Julio) ───────
st.subheader("Análise Visual — Gráficos de Correlação e Distribuição")
st.info(
    "Este espaço está reservado para os gráficos desenvolvidos pela equipe de Análise Visual "
    "(Cauã, Diego, Julio): correlações entre variáveis, mapas de calor e distribuições."
)

st.divider()

# ── Espaço reservado para Design BI (Diego, Julio, Tamires, Vanessa) ──────────
st.subheader("Design BI — Painel Avançado")
st.info(
    "Este espaço está reservado para o painel desenvolvido pela equipe de Design BI "
    "(Diego, Julio, Tamires, Vanessa): visualizações interativas e layout final do dashboard."
)
