import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "base_tratada.csv"

st.set_page_config(
    page_title="Análise preditiva de evasão no ensino superior, Projeto Integrador: Grupo 03 | Senac EAD 2026",
    page_icon="🎓",
    layout="wide",
)

CORES_STATUS = {
    "Permaneceram": "#2E86AB",
    "Evadiram": "#D64545",
}

CORES_BINARIAS = {
    "Não trabalha": "#2E86AB",
    "Trabalha": "#F18F01",
    "Com acesso": "#2E86AB",
    "Sem acesso": "#D64545",
    "Com bolsa": "#6A994E",
    "Sem bolsa": "#8D99AE",
}

ORDEM_ANOS = ["1º ano", "2º ano", "3º ano", "4º ano"]
ORDEM_STATUS = ["Permaneceram", "Evadiram"]


@st.cache_data
def carregar_dados():
    df = pd.read_csv(DATA_FILE)

    colunas_numericas = [
        "Age",
        "Family_Income",
        "Internet_Access",
        "Study_Hours_per_Day",
        "Attendance_Rate",
        "Assignment_Delay_Days",
        "Travel_Time_Minutes",
        "Part_Time_Job",
        "Scholarship",
        "Stress_Index",
        "GPA",
        "Semester_GPA",
        "CGPA",
        "Dropout",
    ]

    for coluna in colunas_numericas:
        if coluna in df.columns:
            df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    df = df.dropna(subset=["Age", "Department", "Semester", "Dropout"])
    df["Dropout"] = df["Dropout"].astype(int)
    df["Idade"] = df["Age"].round().astype(int)

    df["Status_Evasao"] = df["Dropout"].map({
        0: "Permaneceram",
        1: "Evadiram",
    })

    df["Genero"] = df["Gender"].map({
        "Male": "Masculino",
        "Female": "Feminino",
    }).fillna(df["Gender"])

    df["Acesso_Internet"] = df["Internet_Access"].map({
        0: "Sem acesso",
        1: "Com acesso",
    })

    df["Trabalho"] = df["Part_Time_Job"].map({
        0: "Não trabalha",
        1: "Trabalha",
    })

    df["Bolsa"] = df["Scholarship"].map({
        0: "Sem bolsa",
        1: "Com bolsa",
    })

    mapa_departamentos = {
        "Engineering": "Engenharia",
        "Arts": "Artes",
        "CS": "Ciência da Computação",
        "Business": "Negócios",
        "Science": "Ciências",
    }

    mapa_anos = {
        "Year 1": "1º ano",
        "Year 2": "2º ano",
        "Year 3": "3º ano",
        "Year 4": "4º ano",
    }

    mapa_escolaridade = {
        "High School": "Ensino médio",
        "Bachelor": "Graduação",
        "Master": "Mestrado",
        "PhD": "Doutorado",
    }

    df["Departamento"] = df["Department"].map(mapa_departamentos).fillna(df["Department"])
    df["Ano"] = df["Semester"].map(mapa_anos).fillna(df["Semester"])
    df["Escolaridade_Pais"] = df["Parental_Education"].map(mapa_escolaridade).fillna(df["Parental_Education"])

    df["Estresse_Alto"] = df["Stress_Index"].apply(
        lambda valor: "Acima de 6" if valor > 6 else "Até 6"
    )

    return df


def formatar_inteiro(valor):
    if pd.isna(valor):
        return "0"
    return f"{int(valor):,}".replace(",", ".")


def formatar_decimal(valor, casas=1):
    if pd.isna(valor):
        return "0"
    return f"{valor:.{casas}f}".replace(".", ",")


def formatar_percentual(valor, casas=1):
    return f"{formatar_decimal(valor, casas)}%"


def formatar_moeda(valor):
    if pd.isna(valor):
        return "R$ 0"
    return f"R$ {formatar_inteiro(valor)}"


def aplicar_layout(fig, titulo_x=None, titulo_y=None, mostrar_legenda=True):
    fig.update_layout(
        template="plotly_white",
        title_font_size=18,
        xaxis_title=titulo_x,
        yaxis_title=titulo_y,
        legend_title_text="Legenda",
        showlegend=mostrar_legenda,
        margin=dict(l=20, r=20, t=70, b=40),
    )
    return fig


def taxa_evasao_por_grupo(df_base, coluna):
    if df_base.empty or coluna not in df_base.columns:
        return pd.DataFrame(columns=[coluna, "Evadiram", "Total", "Taxa de Evasão (%)"])

    base = df_base.dropna(subset=[coluna]).copy()

    if base.empty:
        return pd.DataFrame(columns=[coluna, "Evadiram", "Total", "Taxa de Evasão (%)"])

    resultado = (
        base.groupby(coluna, observed=False)["Dropout"]
        .agg(Evadiram="sum", Total="count")
        .assign(**{"Taxa de Evasão (%)": lambda x: x["Evadiram"] / x["Total"] * 100})
        .sort_values("Taxa de Evasão (%)", ascending=False)
        .reset_index()
    )

    resultado["Taxa de Evasão (%)"] = resultado["Taxa de Evasão (%)"].round(1)
    return resultado


def media_por_status(df_base, coluna):
    if df_base.empty:
        return pd.Series(dtype=float)

    return (
        df_base.groupby("Status_Evasao")[coluna]
        .mean()
        .reindex(ORDEM_STATUS)
        .dropna()
        .round(2)
    )


def criar_faixas_renda(df_base):
    df_renda = df_base.copy()

    if df_renda["Family_Income"].nunique() <= 1:
        df_renda["Faixa de renda"] = "Faixa única"
        return df_renda

    df_renda["Faixa de renda"] = pd.qcut(
        df_renda["Family_Income"],
        q=5,
        duplicates="drop",
    )

    df_renda["Faixa de renda"] = df_renda["Faixa de renda"].astype(str)
    return df_renda


def grafico_barra_horizontal(df_plot, coluna_categoria, coluna_valor, titulo, titulo_x, titulo_y, escala="Reds"):
    df_temp = df_plot.sort_values(coluna_valor, ascending=True).copy()

    fig = px.bar(
        df_temp,
        x=coluna_valor,
        y=coluna_categoria,
        orientation="h",
        color=coluna_valor,
        text=coluna_valor,
        title=titulo,
        color_continuous_scale=escala,
    )

    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig = aplicar_layout(
        fig,
        titulo_x=titulo_x,
        titulo_y=titulo_y,
        mostrar_legenda=False,
    )

    return fig


df = carregar_dados()

st.title("📊🎓 Análise preditiva de evasão no ensino superior")
st.caption("Projeto Integrador: Desenvolvimento Low Code em Ciência de Dados - Grupo 03 | Senac EAD 2026")

st.sidebar.header("Filtros")

anos_existentes = [ano for ano in ORDEM_ANOS if ano in df["Ano"].dropna().unique().tolist()]
anos_restantes = sorted([ano for ano in df["Ano"].dropna().unique().tolist() if ano not in anos_existentes])
anos = anos_existentes + anos_restantes

departamentos = sorted(df["Departamento"].dropna().unique().tolist())
generos = sorted(df["Genero"].dropna().unique().tolist())
educacao_pais = sorted(df["Escolaridade_Pais"].dropna().unique().tolist())

idade_min = int(df["Age"].min())
idade_max = int(df["Age"].max())

renda_min = int(df["Family_Income"].min())
renda_max = int(df["Family_Income"].max())

departamento_selecionado = st.sidebar.selectbox(
    "Departamento",
    options=["Todos"] + departamentos,
)

ano_selecionado = st.sidebar.selectbox(
    "Ano do curso",
    options=["Todos"] + anos,
)

genero_selecionado = st.sidebar.selectbox(
    "Gênero",
    options=["Todos"] + generos,
)

educacao_selecionada = st.sidebar.selectbox(
    "Escolaridade dos pais",
    options=["Todos"] + educacao_pais,
)

faixa_idade = st.sidebar.slider(
    "Faixa etária",
    min_value=idade_min,
    max_value=idade_max,
    value=(idade_min, idade_max),
)

faixa_renda = st.sidebar.slider(
    "Faixa de renda familiar",
    min_value=renda_min,
    max_value=renda_max,
    value=(renda_min, renda_max),
    step=1000,
)

filtro_trabalho = st.sidebar.selectbox(
    "Trabalho parcial",
    options=["Todos", "Trabalha", "Não trabalha"],
)

filtro_internet = st.sidebar.selectbox(
    "Acesso à internet",
    options=["Todos", "Com acesso", "Sem acesso"],
)

filtro_bolsa = st.sidebar.selectbox(
    "Bolsa de estudos",
    options=["Todos", "Com bolsa", "Sem bolsa"],
)

amostra_minima_idade = st.sidebar.slider(
    "Amostra mínima por idade no ranking",
    min_value=1,
    max_value=100,
    value=20,
)

df_filtrado = df.copy()

if departamento_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Departamento"] == departamento_selecionado]

if ano_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Ano"] == ano_selecionado]

if genero_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Genero"] == genero_selecionado]

if educacao_selecionada != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Escolaridade_Pais"] == educacao_selecionada]

df_filtrado = df_filtrado[
    (df_filtrado["Age"] >= faixa_idade[0]) &
    (df_filtrado["Age"] <= faixa_idade[1])
]

df_filtrado = df_filtrado[
    (df_filtrado["Family_Income"] >= faixa_renda[0]) &
    (df_filtrado["Family_Income"] <= faixa_renda[1])
]

if filtro_trabalho != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Trabalho"] == filtro_trabalho]

if filtro_internet != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Acesso_Internet"] == filtro_internet]

if filtro_bolsa != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Bolsa"] == filtro_bolsa]

if df_filtrado.empty:
    st.warning("Nenhum registro encontrado com os filtros selecionados.")
    st.stop()

total_alunos = len(df_filtrado)
total_evadidos = int(df_filtrado["Dropout"].sum())
total_permaneceram = total_alunos - total_evadidos
taxa_geral = total_evadidos / total_alunos * 100 if total_alunos > 0 else 0
media_cgpa = df_filtrado["CGPA"].mean()
media_presenca = df_filtrado["Attendance_Rate"].mean()
media_renda = df_filtrado["Family_Income"].mean()

st.subheader("📌 Visão geral")

st.markdown(
    """
Este dashboard é uma análise preditiva de fatores associados à evasão acadêmica a partir de uma base de dados estudantil.
A proposta é combinar filtros interativos com gráficos comparativos, distribuições, correlações e conclusões por seção, possibilitando uma estrutura analítica capaz de indicar qual perfil de aluno apresenta maior risco de evasão para adoção de medidas preventivas.
"""
)

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Total de alunos", formatar_inteiro(total_alunos))
col2.metric("Evadiram", formatar_inteiro(total_evadidos))
col3.metric("Taxa de evasão", formatar_percentual(taxa_geral))
col4.metric("CGPA médio", formatar_decimal(media_cgpa, 2))
col5.metric("Presença média", formatar_percentual(media_presenca))
col6.metric("Renda média", formatar_moeda(media_renda))

status_df = pd.DataFrame({
    "Status": ["Permaneceram", "Evadiram"],
    "Quantidade": [total_permaneceram, total_evadidos],
})

fig_rosca_status = px.pie(
    status_df,
    names="Status",
    values="Quantidade",
    hole=0.55,
    title="🔎 Composição geral:",
    color="Status",
    color_discrete_map=CORES_STATUS,
)

fig_rosca_status.update_traces(
    textposition="inside",
    textinfo="percent+label",
)

fig_rosca_status.update_layout(
    template="plotly_white",
    title_font_size=18,
    legend_title_text="Status",
    margin=dict(l=20, r=20, t=70, b=40),
)

st.plotly_chart(fig_rosca_status, width="stretch")

st.info(
    f"O panorama geral mostra que a taxa de escape acadêmica no cenário filtrado é de {formatar_percentual(taxa_geral)}. Os indicadores ilustrados demonstram que fatores como desempenho acadêmico, frequência, estresse, renda familiar e condições de estudo possuem relação direta com a permanência dos alunos na instituição. A partir dos filtros interativos e das comparações estatísticas, é possível identificar perfis com maior tendência à evasão, contribuindo para ações preventivas e estratégias de acompanhamento estudantil mais eficientes."
)

st.divider()

st.subheader("1. ⏱️ Presença: ")
st.markdown(" Os alunos que evadiram apresentam presença menor do que os que permaneceram?")

presenca_status = media_por_status(df_filtrado, "Attendance_Rate")
presenca_df = presenca_status.reset_index()
presenca_df.columns = ["Status", "Presença média (%)"]

presenca_permaneceu = presenca_status.get("Permaneceram", pd.NA)
presenca_evadiu = presenca_status.get("Evadiram", pd.NA)

p1, p2, p3 = st.columns(3)

p1.metric(
    "Presença média, permaneceram",
    formatar_percentual(presenca_permaneceu) if pd.notna(presenca_permaneceu) else "Sem dados",
)

p2.metric(
    "Presença média, evadiram",
    formatar_percentual(presenca_evadiu) if pd.notna(presenca_evadiu) else "Sem dados",
)

if pd.notna(presenca_permaneceu) and pd.notna(presenca_evadiu):
    p3.metric("Diferença", f"{formatar_decimal(presenca_permaneceu - presenca_evadiu)} p.p.")
else:
    p3.metric("Diferença", "Sem dados")

box_col, bar_col = st.columns(2)

with box_col:
    fig_box_presenca = px.box(
        df_filtrado,
        x="Status_Evasao",
        y="Attendance_Rate",
        color="Status_Evasao",
        title="Distribuição da presença por status de evasão",
        color_discrete_map=CORES_STATUS,
        points=False,
    )

    fig_box_presenca = aplicar_layout(
        fig_box_presenca,
        titulo_x="Status do aluno",
        titulo_y="Presença (%)",
        mostrar_legenda=False,
    )

    st.plotly_chart(fig_box_presenca, width="stretch")

with bar_col:
    fig_bar_presenca = px.bar(
        presenca_df,
        x="Status",
        y="Presença média (%)",
        color="Status",
        text="Presença média (%)",
        title="Presença média por status de evasão",
        color_discrete_map=CORES_STATUS,
    )

    fig_bar_presenca.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_bar_presenca = aplicar_layout(
        fig_bar_presenca,
        titulo_x="Status do aluno",
        titulo_y="Presença média (%)",
        mostrar_legenda=False,
    )

    st.plotly_chart(fig_bar_presenca, width="stretch")

if pd.notna(presenca_permaneceu) and pd.notna(presenca_evadiu):
    if presenca_evadiu < presenca_permaneceu:
        st.info(
            f"Os dados mostram que a frequência acadêmica apresenta grande relação com a permanência dos estudantes no ensino superior. Os alunos que permaneceram apresentaram média de presença de {formatar_percentual(presenca_permaneceu)}, enquanto os alunos que evadiram registraram média de {formatar_percentual(presenca_evadiu)}. Essa diferença reforça a hipótese de que baixos índices de presença podem estar associados à redução do engajamento acadêmico, dificuldades de adaptação e maior risco de abandono do curso. Os dados mostram que a frequência acadêmica apresenta grande relação com a permanência dos estudantes no ensino superior. Os alunos que permaneceram apresentaram média de presença de {formatar_percentual(presenca_permaneceu)}, enquanto os alunos que evadiram registraram média de {formatar_percentual(presenca_evadiu)}. Essa diferença reforça a hipótese de que baixos índices de presença podem estar associados à redução do engajamento acadêmico, dificuldades de adaptação e maior risco de abandono do curso."
        )
    else:
        st.info(
           "No trecho analisado, não foi identificada diferença significativa entre a média de presença dos alunos que permaneceram e daqueles que evadiram. Isso mostra que outros fatores podem ter exercido maior influência sobre a evasão acadêmica neste cenário específico."
        )

st.divider()

st.subheader("2. 👥 Faixa etária: ")
st.markdown("Quais idades têm maior taxa de evasão e em quais anos há mais abandono?")

top_idades = (
    df_filtrado.groupby("Idade")["Dropout"]
    .agg(Evadiram="sum", Total="count")
    .assign(**{"Taxa de Evasão (%)": lambda x: x["Evadiram"] / x["Total"] * 100})
    .query("Total >= @amostra_minima_idade")
    .sort_values("Taxa de Evasão (%)", ascending=False)
    .head(10)
    .reset_index()
)

top_idades["Taxa de Evasão (%)"] = top_idades["Taxa de Evasão (%)"].round(1)

evasoes_por_ano = (
    df_filtrado[df_filtrado["Dropout"] == 1]
    .groupby("Ano")
    .size()
    .reindex(anos, fill_value=0)
    .reset_index()
)

evasoes_por_ano.columns = ["Ano", "Quantidade de evasões"]

taxa_por_ano = taxa_evasao_por_grupo(df_filtrado, "Ano")
taxa_por_ano["Ano"] = pd.Categorical(taxa_por_ano["Ano"], categories=anos, ordered=True)
taxa_por_ano = taxa_por_ano.sort_values("Ano")

idade_col, ano_col = st.columns(2)

with idade_col:
    if top_idades.empty:
        st.info("Não há idades com a amostra mínima definida no filtro lateral.")
    else:
        fig_idades = grafico_barra_horizontal(
            top_idades,
            coluna_categoria="Idade",
            coluna_valor="Taxa de Evasão (%)",
            titulo="Dez idades com maior taxa de evasão",
            titulo_x="Taxa de evasão (%)",
            titulo_y="Idade",
            escala="Reds",
        )

        st.plotly_chart(fig_idades, width="stretch")
        st.dataframe(top_idades, width="stretch", hide_index=True)

with ano_col:
    fig_ano = px.bar(
        evasoes_por_ano,
        x="Ano",
        y="Quantidade de evasões",
        text="Quantidade de evasões",
        title="Quantidade de evasões por ano do curso",
        color="Quantidade de evasões",
        color_continuous_scale="Oranges",
    )

    fig_ano.update_traces(textposition="outside")
    fig_ano = aplicar_layout(
        fig_ano,
        titulo_x="Ano do curso",
        titulo_y="Quantidade de evasões",
        mostrar_legenda=False,
    )

    st.plotly_chart(fig_ano, width="stretch")
    st.dataframe(taxa_por_ano, width="stretch", hide_index=True)

if not top_idades.empty and not taxa_por_ano.empty:
    idade_critica = top_idades.iloc[0]["Idade"]
    taxa_idade_critica = top_idades.iloc[0]["Taxa de Evasão (%)"]

    taxa_por_ano_ranking = taxa_por_ano.sort_values("Taxa de Evasão (%)", ascending=False)
    ano_critico = taxa_por_ano_ranking.iloc[0]["Ano"]
    taxa_ano_critico = taxa_por_ano_ranking.iloc[0]["Taxa de Evasão (%)"]
#2_Faixa_Etaria_Conclusao
    st.info(
        "No trecho analisado, não foi identificada diferença significativa entre a média de presença dos alunos que permaneceram e daqueles que evadiram. Isso mostra que outros fatores podem ter exercido maior influência sobre a evasão acadêmica neste cenário específico."
    )

st.divider()

st.subheader("3. 🧠 Estresse e desempenho: ")
st.markdown("Evadidos têm pior desempenho e maior estresse?")

alunos_estresse_alto = df_filtrado[df_filtrado["Stress_Index"] > 6]
qtd_estresse_alto = len(alunos_estresse_alto)
cgpa_estresse_alto = alunos_estresse_alto["CGPA"].mean()
taxa_evasao_estresse_alto = alunos_estresse_alto["Dropout"].mean() * 100 if qtd_estresse_alto > 0 else 0

e1, e2, e3 = st.columns(3)

e1.metric("Alunos com estresse acima de 6", formatar_inteiro(qtd_estresse_alto))
e2.metric(
    "CGPA médio nesse grupo",
    formatar_decimal(cgpa_estresse_alto, 2) if qtd_estresse_alto > 0 else "Sem dados",
)
e3.metric(
    "Taxa de evasão nesse grupo",
    formatar_percentual(taxa_evasao_estresse_alto) if qtd_estresse_alto > 0 else "Sem dados",
)

cgpa_col, stress_col = st.columns(2)

with cgpa_col:
    fig_box_cgpa = px.box(
        df_filtrado,
        x="Status_Evasao",
        y="CGPA",
        color="Status_Evasao",
        title="Distribuição do CGPA por status de evasão",
        color_discrete_map=CORES_STATUS,
        points=False,
    )

    fig_box_cgpa = aplicar_layout(
        fig_box_cgpa,
        titulo_x="Status do aluno",
        titulo_y="CGPA",
        mostrar_legenda=False,
    )

    st.plotly_chart(fig_box_cgpa, width="stretch")

with stress_col:
    fig_box_estresse = px.box(
        df_filtrado,
        x="Status_Evasao",
        y="Stress_Index",
        color="Status_Evasao",
        title="Distribuição do estresse por status de evasão",
        color_discrete_map=CORES_STATUS,
        points=False,
    )

    fig_box_estresse = aplicar_layout(
        fig_box_estresse,
        titulo_x="Status do aluno",
        titulo_y="Índice de estresse",
        mostrar_legenda=False,
    )

    st.plotly_chart(fig_box_estresse, width="stretch")

media_cgpa_status = media_por_status(df_filtrado, "CGPA")
media_estresse_status = media_por_status(df_filtrado, "Stress_Index")

cgpa_evadiu = media_cgpa_status.get("Evadiram", pd.NA)
cgpa_permaneceu = media_cgpa_status.get("Permaneceram", pd.NA)

estresse_evadiu = media_estresse_status.get("Evadiram", pd.NA)
estresse_permaneceu = media_estresse_status.get("Permaneceram", pd.NA)

if pd.notna(cgpa_evadiu) and pd.notna(cgpa_permaneceu) and pd.notna(estresse_evadiu) and pd.notna(estresse_permaneceu):
    st.info(
        #Estresse e desempenho
        f"Os dados evideciam que alunos que saíram atingiram desempenho acadêmico inferior e níveis de estresse mais elevados em comparação aos que permaneceram. O CGPA médio dos alunos evadidos foi de {formatar_decimal(cgpa_evadiu,2)}, enquanto os estudantes que permaneceram registraram média superior. Em relação ao estresse, os alunos evadidos apresentaram média de {formatar_decimal(estresse_evadiu,2)}, evidenciando possível impacto emocional e acadêmico no processo de permanência universitária. Esses dados validam a importância de iniciativas voltadas ao apoio psicológico e ao acompanhamento do desempenho estudantil."

    )

st.divider()

st.subheader("4. 💼 Trabalho de meio período:")
st.markdown("Alunos que trabalham apresentam mais estresse ou evasão?")

estresse_por_trabalho = (
    df_filtrado.groupby("Trabalho")["Stress_Index"]
    .mean()
    .reindex(["Não trabalha", "Trabalha"])
    .dropna()
    .round(2)
    .reset_index()
)

estresse_por_trabalho.columns = ["Trabalho parcial", "Estresse médio"]

taxa_evasao_trabalho = taxa_evasao_por_grupo(df_filtrado, "Trabalho")

trab_col1, trab_col2 = st.columns(2)

with trab_col1:
    fig_box_trabalho = px.box(
        df_filtrado,
        x="Trabalho",
        y="Stress_Index",
        color="Trabalho",
        title="Distribuição do estresse por trabalho parcial",
        color_discrete_map=CORES_BINARIAS,
        points=False,
    )

    fig_box_trabalho = aplicar_layout(
        fig_box_trabalho,
        titulo_x="Trabalho parcial",
        titulo_y="Índice de estresse",
        mostrar_legenda=False,
    )

    st.plotly_chart(fig_box_trabalho, width="stretch")

with trab_col2:
    fig_bar_trabalho = px.bar(
        taxa_evasao_trabalho,
        x="Trabalho",
        y="Taxa de Evasão (%)",
        color="Trabalho",
        text="Taxa de Evasão (%)",
        title="Taxa de evasão por trabalho parcial",
        color_discrete_map=CORES_BINARIAS,
    )

    fig_bar_trabalho.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_bar_trabalho = aplicar_layout(
        fig_bar_trabalho,
        titulo_x="Trabalho parcial",
        titulo_y="Taxa de evasão (%)",
        mostrar_legenda=False,
    )

    st.plotly_chart(fig_bar_trabalho, width="stretch")
    st.dataframe(taxa_evasao_trabalho, width="stretch", hide_index=True)

if not taxa_evasao_trabalho.empty and not estresse_por_trabalho.empty:
    trabalho_mais_evasao = taxa_evasao_trabalho.iloc[0]["Trabalho"]
    taxa_trabalho_mais_evasao = taxa_evasao_trabalho.iloc[0]["Taxa de Evasão (%)"]

    st.info(
        #TRABALHO MEIO PERIODO
        f"A análise relacionada ao trabalho de meio período evidencia que o grupo '{trabalho_mais_evasao}' mostrou a maior taxa de evasão, atingindo {formatar_percentual(taxa_trabalho_mais_evasao)}. Os resultados sugerem que a necessidade de conciliar atividades profissionais e acadêmicas pode influenciar diretamente o desempenho, os níveis de estresse e a permanência dos estudantes no curso, especialmente em contextos de maior carga horária ou dificuldade financeira."
    )

st.divider()

st.subheader("5. 💰 Perfil socioeconômico:")
st.markdown("Bolsa de estudos, renda e escolaridade dos pais mudam o perfil de evasão?")

df_renda = criar_faixas_renda(df_filtrado)

taxa_por_renda = taxa_evasao_por_grupo(df_renda, "Faixa de renda")
taxa_por_bolsa = taxa_evasao_por_grupo(df_filtrado, "Bolsa")
taxa_por_escolaridade = taxa_evasao_por_grupo(df_filtrado, "Escolaridade_Pais")

bolsa_contagem = (
    df_filtrado["Bolsa"]
    .value_counts()
    .reindex(["Com bolsa", "Sem bolsa"])
    .fillna(0)
    .reset_index()
)

bolsa_contagem.columns = ["Bolsa", "Quantidade"]

socio1, socio2 = st.columns(2)

with socio1:
    fig_rosca_bolsa = px.pie(
        bolsa_contagem,
        names="Bolsa",
        values="Quantidade",
        hole=0.55,
        title="Composição dos alunos por bolsa de estudos",
        color="Bolsa",
        color_discrete_map=CORES_BINARIAS,
    )

    fig_rosca_bolsa.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    fig_rosca_bolsa.update_layout(
        template="plotly_white",
        title_font_size=18,
        legend_title_text="Bolsa",
        margin=dict(l=20, r=20, t=70, b=40),
    )

    st.plotly_chart(fig_rosca_bolsa, width="stretch")

with socio2:
    fig_bar_bolsa = px.bar(
        taxa_por_bolsa,
        x="Bolsa",
        y="Taxa de Evasão (%)",
        color="Bolsa",
        text="Taxa de Evasão (%)",
        title="Taxa de evasão por bolsa de estudos",
        color_discrete_map=CORES_BINARIAS,
    )

    fig_bar_bolsa.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_bar_bolsa = aplicar_layout(
        fig_bar_bolsa,
        titulo_x="Bolsa de estudos",
        titulo_y="Taxa de evasão (%)",
        mostrar_legenda=False,
    )

    st.plotly_chart(fig_bar_bolsa, width="stretch")

renda_col, escolaridade_col = st.columns(2)

with renda_col:
    if taxa_por_renda.empty:
        st.info("Não há dados suficientes para formar faixas de renda no recorte atual.")
    else:
        fig_renda = px.bar(
            taxa_por_renda,
            x="Faixa de renda",
            y="Taxa de Evasão (%)",
            color="Taxa de Evasão (%)",
            text="Taxa de Evasão (%)",
            title="Taxa de evasão por faixa de renda familiar",
            color_continuous_scale="Blues",
        )

        fig_renda.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_renda = aplicar_layout(
            fig_renda,
            titulo_x="Faixa de renda familiar",
            titulo_y="Taxa de evasão (%)",
            mostrar_legenda=False,
        )

        st.plotly_chart(fig_renda, width="stretch")
        st.dataframe(taxa_por_renda, width="stretch", hide_index=True)

with escolaridade_col:
    fig_escolaridade = grafico_barra_horizontal(
        taxa_por_escolaridade,
        coluna_categoria="Escolaridade_Pais",
        coluna_valor="Taxa de Evasão (%)",
        titulo="Taxa de evasão por escolaridade dos pais",
        titulo_x="Taxa de evasão (%)",
        titulo_y="Escolaridade dos pais",
        escala="Purples",
    )

    st.plotly_chart(fig_escolaridade, width="stretch")
    st.dataframe(taxa_por_escolaridade, width="stretch", hide_index=True)

if not taxa_por_renda.empty:
    faixa_renda_critica = taxa_por_renda.iloc[0]["Faixa de renda"]
    taxa_renda_critica = taxa_por_renda.iloc[0]["Taxa de Evasão (%)"]

    st.info(
        f"Os indicadores socioeconômicos analisados evidencia que a faixa de renda '{faixa_renda_critica}' revelou a maior taxa de evasão, registrando {formatar_percentual(taxa_renda_critica)}. Além disso, fatores como acesso à bolsa de estudos e nível de escolaridade dos pais também demonstraram influência sobre a permanência acadêmica. Os resultados evidenciam que condições socioeconômicas podem impactar diretamente a continuidade dos estudos e o acesso a melhores oportunidades educacionais."
    )

st.divider()

st.subheader("6. 🏫 Departamento:")
st.markdown("Qual departamento apresenta maior taxa de abandono?")

taxa_por_departamento = taxa_evasao_por_grupo(df_filtrado, "Departamento")

fig_departamento = grafico_barra_horizontal(
    taxa_por_departamento,
    coluna_categoria="Departamento",
    coluna_valor="Taxa de Evasão (%)",
    titulo="Taxa de evasão por departamento",
    titulo_x="Taxa de evasão (%)",
    titulo_y="Departamento",
    escala="Reds",
)

st.plotly_chart(fig_departamento, width="stretch")
st.dataframe(taxa_por_departamento, width="stretch", hide_index=True)

if not taxa_por_departamento.empty:
    departamento_critico = taxa_por_departamento.iloc[0]

    st.info(
        f"Entre os departamentos analisados, {departamento_critico['Departamento']} apresentou a maior taxa de evasão, alcançando {formatar_percentual(departamento_critico['Taxa de Evasão (%)'])}. Esse comportamento pode estar relacionado a fatores específicos da área, como nível de exigência acadêmica, adaptação curricular ou perfil dos estudantes. Os resultados reforçam a importância de estratégias direcionadas para acompanhamento e retenção dos alunos nesse departamento."
    )

st.divider()

st.subheader("7. 🧮 Correlação: ")
st.markdown("Quais variáveis têm maior associação estatística com evasão?")

colunas_correlacao = [
    "Age",
    "Family_Income",
    "Internet_Access",
    "Study_Hours_per_Day",
    "Attendance_Rate",
    "Assignment_Delay_Days",
    "Travel_Time_Minutes",
    "Part_Time_Job",
    "Scholarship",
    "Stress_Index",
    "GPA",
    "Semester_GPA",
    "CGPA",
    "Dropout",
]

rotulos_correlacao = {
    "Age": "Idade",
    "Family_Income": "Renda familiar",
    "Internet_Access": "Acesso à internet",
    "Study_Hours_per_Day": "Horas de estudo",
    "Attendance_Rate": "Presença",
    "Assignment_Delay_Days": "Atraso em atividades",
    "Travel_Time_Minutes": "Tempo de deslocamento",
    "Part_Time_Job": "Trabalho parcial",
    "Scholarship": "Bolsa",
    "Stress_Index": "Estresse",
    "GPA": "GPA",
    "Semester_GPA": "GPA do semestre",
    "CGPA": "CGPA",
    "Dropout": "Evasão",
}

colunas_correlacao = [col for col in colunas_correlacao if col in df_filtrado.columns]
correlacao = df_filtrado[colunas_correlacao].corr(numeric_only=True)

correlacao_dropout = (
    correlacao["Dropout"]
    .drop("Dropout")
    .sort_values(key=lambda serie: serie.abs(), ascending=False)
    .round(3)
    .reset_index()
)

correlacao_dropout.columns = ["Variável", "Correlação com evasão"]
correlacao_dropout["Variável"] = (
    correlacao_dropout["Variável"]
    .map(rotulos_correlacao)
    .fillna(correlacao_dropout["Variável"])
)

correlacao_pt = correlacao.rename(
    index=rotulos_correlacao,
    columns=rotulos_correlacao,
)

corr_col1, corr_col2 = st.columns(2)

with corr_col1:
    fig_corr_bar = grafico_barra_horizontal(
        correlacao_dropout,
        coluna_categoria="Variável",
        coluna_valor="Correlação com evasão",
        titulo="Correlação das variáveis com evasão",
        titulo_x="Correlação com evasão",
        titulo_y="Variável",
        escala="RdBu_r",
    )

    fig_corr_bar.update_traces(texttemplate="%{text:.3f}")
    st.plotly_chart(fig_corr_bar, width="stretch")
    st.dataframe(correlacao_dropout, width="stretch", hide_index=True)

with corr_col2:
    fig_heatmap = px.imshow(
        correlacao_pt,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        title="Mapa de calor da matriz de correlação",
        aspect="auto",
    )

    fig_heatmap.update_layout(
        template="plotly_white",
        title_font_size=18,
        margin=dict(l=20, r=20, t=70, b=40),
    )

    st.plotly_chart(fig_heatmap, width="stretch")

if not correlacao_dropout.empty:
    variavel_mais_associada = correlacao_dropout.iloc[0]["Variável"]
    valor_correlacao = correlacao_dropout.iloc[0]["Correlação com evasão"]

    st.info(
        f"A variável '{variavel_mais_associada}' apresentou a maior associação estatística com a evasão, registrando correlação de {formatar_decimal(valor_correlacao,3)}. Embora a correlação não represente causalidade, o resultado demonstra que essa variável possui forte relação com o comportamento de evasão observado na base analisada. Dessa forma, ela pode ser considerada um importante indicador para estudos preditivos e monitoramento acadêmico."
           )

st.divider()

st.subheader("8. 🧩 Análise agregada, bolhas por departamento")
st.markdown(
    "Como os departamentos se posicionam quando combinamos desempenho, estresse e evasão?"
)

bolhas_departamento = (
    df_filtrado.groupby("Departamento")
    .agg(
        Total=("Student_ID", "count"),
        Evadiram=("Dropout", "sum"),
        CGPA_medio=("CGPA", "mean"),
        Estresse_medio=("Stress_Index", "mean"),
        Presenca_media=("Attendance_Rate", "mean"),
    )
    .reset_index()
)

bolhas_departamento["Taxa de Evasão (%)"] = (
    bolhas_departamento["Evadiram"] / bolhas_departamento["Total"] * 100
).round(1)

bolhas_departamento["CGPA_medio"] = bolhas_departamento["CGPA_medio"].round(2)
bolhas_departamento["Estresse_medio"] = bolhas_departamento["Estresse_medio"].round(2)
bolhas_departamento["Presenca_media"] = bolhas_departamento["Presenca_media"].round(1)

fig_bolhas = px.scatter(
    bolhas_departamento,
    x="CGPA_medio",
    y="Estresse_medio",
    size="Taxa de Evasão (%)",
    color="Taxa de Evasão (%)",
    hover_name="Departamento",
    hover_data={
        "Total": True,
        "Evadiram": True,
        "Presenca_media": True,
        "CGPA_medio": True,
        "Estresse_medio": True,
        "Taxa de Evasão (%)": True,
    },
    title="Bolhas por departamento, CGPA médio, estresse médio e taxa de evasão",
    color_continuous_scale="Reds",
    size_max=55,
)

fig_bolhas = aplicar_layout(
    fig_bolhas,
    titulo_x="CGPA médio",
    titulo_y="Estresse médio",
    mostrar_legenda=False,
)

st.plotly_chart(fig_bolhas, width="stretch")
st.dataframe(bolhas_departamento, width="stretch", hide_index=True)

if not bolhas_departamento.empty:
    departamento_maior_evasao = bolhas_departamento.sort_values(
        "Taxa de Evasão (%)",
        ascending=False,
    ).iloc[0]

    st.info(
        f"A análise agregada dos departamentos demonstra que {departamento_maior_evasao['Departamento']} apresentou a maior taxa de evasão, com {formatar_percentual(departamento_maior_evasao['Taxa de Evasão (%)'])}. Observando conjuntamente os indicadores de desempenho acadêmico, estresse e frequência, é possível perceber que departamentos com maiores níveis de estresse e menor rendimento tendem a concentrar índices mais elevados de evasão. Essa visualização facilita a identificação de áreas que demandam maior atenção institucional."
    )

st.divider()

st.subheader("9. 🗂️ Dados filtrados:")

colunas_tabela = [
    "Student_ID",
    "Age",
    "Genero",
    "Departamento",
    "Ano",
    "Family_Income",
    "Attendance_Rate",
    "Stress_Index",
    "GPA",
    "Semester_GPA",
    "CGPA",
    "Trabalho",
    "Acesso_Internet",
    "Bolsa",
    "Escolaridade_Pais",
    "Status_Evasao",
]

tabela = df_filtrado[colunas_tabela].copy()

tabela = tabela.rename(columns={
    "Student_ID": "ID do aluno",
    "Age": "Idade original",
    "Family_Income": "Renda familiar",
    "Attendance_Rate": "Presença (%)",
    "Stress_Index": "Índice de estresse",
    "GPA": "GPA",
    "Semester_GPA": "GPA do semestre",
    "CGPA": "CGPA",
    "Escolaridade_Pais": "Escolaridade dos pais",
    "Status_Evasao": "Status de evasão",
})

st.dataframe(tabela, width="stretch", hide_index=True)

st.caption(
    "Observação: indicadores, gráficos, tabelas e conclusões são recalculados automaticamente conforme os filtros selecionados."
)