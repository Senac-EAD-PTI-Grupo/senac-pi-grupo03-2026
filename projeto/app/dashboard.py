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

# ── Engajamento e Evasão ───────────────────────────────────────────────────────
st.subheader("Engajamento e Evasão — Média de Presença")

presenca_por_status = (
    df_filtrado.groupby("Dropout")["Attendance_Rate"]
    .mean()
    .reset_index()
    .assign(Status=lambda x: x["Dropout"].map({0: "Permaneceram", 1: "Evadiram"}))
    .set_index("Status")["Attendance_Rate"]
    .round(1)
)

col_eng1, col_eng2, col_eng3 = st.columns(3)
if not presenca_por_status.empty:
    perm = presenca_por_status.get("Permaneceram", None)
    evad = presenca_por_status.get("Evadiram", None)
    if perm is not None:
        col_eng1.metric("Presença média — Permaneceram", f"{perm:.1f}%")
    if evad is not None:
        col_eng2.metric("Presença média — Evadiram", f"{evad:.1f}%")
    if perm is not None and evad is not None:
        col_eng3.metric("Diferença", f"{perm - evad:.1f} p.p.")

st.markdown("**Comparação de presença média: permaneceram vs evadiram**")
st.bar_chart(presenca_por_status)

st.divider()

# ── Análise Temporal — Evasão por Semestre ────────────────────────────────────
st.subheader("Perfil Temporal — Abandono por Semestre")

ORDEM_SEMESTRE = ["Year 1", "Year 2", "Year 3", "Year 4"]
semestres_disponiveis = [s for s in ORDEM_SEMESTRE if s in df_filtrado["Semester"].unique()]

evasao_por_semestre = (
    df_filtrado[df_filtrado["Dropout"] == 1]
    .groupby("Semester")
    .size()
    .reindex(semestres_disponiveis, fill_value=0)
    .rename_axis("Semestre")
    .rename("Evasões")
)

taxa_por_semestre = (
    df_filtrado.groupby("Semester")["Dropout"]
    .mean()
    .reindex(semestres_disponiveis, fill_value=0)
    .mul(100)
    .round(1)
    .rename_axis("Semestre")
    .rename("Taxa de Evasão (%)")
)

col_sem1, col_sem2 = st.columns(2)
with col_sem1:
    st.markdown("**Quantidade de evasões por ano/semestre:**")
    st.bar_chart(evasao_por_semestre)
with col_sem2:
    st.markdown("**Taxa de evasão (%) por ano/semestre:**")
    st.bar_chart(taxa_por_semestre)

st.divider()

# ── Análise Visual (Julio Valença) ────────────────────────────────────────────
st.subheader("Análise Visual — Gráficos de Correlação e Distribuição")
st.caption("Desenvolvido por: Julio Valença")

estresse_alto = df_filtrado[df_filtrado["Stress_Index"] > 6]
cgpa_medio_estresse = estresse_alto["CGPA"].mean()
estresse_trabalha = df_filtrado.groupby("Part_Time_Job")["Stress_Index"].mean().reset_index()

col_av1, col_av2 = st.columns(2)

with col_av1:
    st.metric("Média de CGPA (Alunos com Estresse > 6)", f"{cgpa_medio_estresse:.2f}" if not estresse_alto.empty else "—")
    st.markdown("**Distribuição de Notas (CGPA) por Nível de Estresse:**")
    st.scatter_chart(data=df_filtrado, x="Stress_Index", y="CGPA", color="Dropout")

with col_av2:
    st.markdown("**Média de Estresse: Trabalha Meio Período (1) vs Não Trabalha (0):**")
    st.bar_chart(data=estresse_trabalha.set_index("Part_Time_Job")["Stress_Index"])

st.divider()

# ── Design BI (Julio Valença) ─────────────────────────────────────────────────
st.subheader("Design BI — Painel Avançado de Idades")
st.caption("Desenvolvido por: Julio Valença")

top_10_idades = (
    df_filtrado.groupby("Age")["Dropout"]
    .mean()
    .reset_index()
    .sort_values(by="Dropout", ascending=False)
    .head(10)
)
top_10_idades["Taxa_Evasao_%"] = (top_10_idades["Dropout"] * 100).round(1)

st.markdown("**Top 10 Idades com Maior Taxa Proporcional de Evasão:**")
st.dataframe(
    top_10_idades[["Age", "Taxa_Evasao_%"]],
    use_container_width=True,
    hide_index=True,
)
st.bar_chart(data=top_10_idades.set_index("Age")["Taxa_Evasao_%"])
