# 🎓 Análise preditiva de evasão no ensino superior baseada em fatores acadêmicos e socioeconômicos
> **Projeto Integrador: Desenvolvimento Low Code em Ciência de Dados - Grupo 03 | Senac EAD 2026**

## 📌 1. Visão Geral e Contexto
A evasão acadêmica é um problema social relevante, pois compromete a formação de capital humano e limita o desenvolvimento de um país no longo prazo. As causas da desistência deixam indícios nos dados, como queda no desempenho acadêmico e baixo engajamento dos estudantes. Neste projeto, aplicamos técnicas de Ciência de Dados para identificar esses padrões. A partir de um dataset simulado, desenvolvemos uma estrutura analítica capaz de indicar quais alunos apresentam maior risco de evasão, possibilitando que a instituição adote medidas preventivas antes que o abandono ocorra.


## 👥 2. Equipe de Desenvolvimento

- [Bianca da Silva](https://github.com/bsilva2790-ux)
- [Cauã Silva Macedo](https://github.com/macedoz)
- [Diego Dias de Araujo]()
- [Fábio Gomes da Silva](https://github.com/fabiogomes95)
- [Julio Valença de Azevedo Junior](https://github.com/julio-valenca)
- [Ricardo Augusto Mazzarioli Ribeiro Nunes](https://github.com/ricmazz)
- [Tamires Chorense Nunes Garrones](https://github.com/tamireschorense-dev)
- [Vanessa Byork Ferreira Pinto](https://github.com/Byorks)


## 🎯 3. Objetivo do Projeto

O objetivo é desenvolver um script de processamento de dados para o dataset Student Dropout Prediction. O foco está na construção da lógica de tratamento e na visualização dos fatores que influenciam a evasão acadêmica.

### 3.1. Entregas previstas:

3.1.1 Questões de Análise (Perguntas de Negócio):

- Engajamento e Evasão: Qual a média de presença dos alunos que abandonaram o curso comparada aos que permaneceram?

- Perfil Demográfico e Temporal: Quais são as 10 idades com maior taxa de evasão e em quais semestres o abandono é mais frequente?

- Saúde Mental e Desempenho: Qual a média do CGPA (nota acumulada) dos alunos com nível de estresse acima de 6?

- Impacto do Trabalho: Qual a diferença no nível de estresse entre alunos que trabalham e os que não trabalham?

- Análise Institucional: Qual departamento apresenta a maior taxa de abandono?

3.1.2. Entregas Técnicas:

- Processamento: Script em Python (Pandas) para limpeza do dataset e cálculo das métricas de estresse, presença e notas.

- Visualização: Dashboard em Streamlit com filtros interativos para explorar as taxas de evasão por departamento e idade.

## 📅 4. Planejamento e Organização

### 4.1. Cronograma e Atribuições de Equipe
O cronograma foi dividido em fases para garantir a entrega do pipeline completo:

| Categoria | Atividade | Responsáveis | Status |
| :--- | :--- | :--- | :---: |
| **Gestão** | Criação e organização do Repositório | Ricardo | ✅ |
| **Dados** | Escolha da base [Student Dropout Prediction](https://www.kaggle.com/datasets/meharshanali/student-dropout-prediction-dataset/data) | Todos os integrantes | ✅ |
| **Visão geral** | Contextualização | Tamires | ✅ |
| **Estratégia** | Definição dos Objetivos  | Todos os participantes | ✅ |
| **Engenharia** | Mapeamento dos dados | Ricardo, Tamires, Vanessa | ✅ |
| **Coleta** | Leitura do dataset e Extração dos dados | Bianca, Fábio | ⏳ |
| **Tratamento** | Transformação (Limpeza e Cálculos) | Ricardo, Fábio, Vanessa | ⏳ |
| **Integração** | Carga (Conexão com Dashboard) | Bianca, Cauã, Ricardo | ⏳ |
| **Qualidade** | Monitoramento e Revisão | Cauã, Vanessa | 📅 |
| **Design BI** | Planeamento e Criação do Dashboard | Diego, Julio, Tamires | 📅 |
| **Análise Visual** | Gráficos de correlação e distribuição | Cauã, Diego, Julio | 📅 |
| **Docs** | Organização do README e Documentação | Ricardo, Tamires | ⏳ |
 * Legenda: ✅ Concluído | ⏳ Em andamento | 📅 Planejado

### 4.2. Detalhamento das Etapas Técnicas

Para garantir a clareza do fluxo de trabalho, definimos os seguintes escopos:

- Tratamento: Limpeza de valores nulos, normalização de notas e conversão de variáveis categóricas (como renda) para análise estatística.

- Integração: Automatização do fluxo de dados tratados para o ambiente do Streamlit, garantindo a atualização em tempo real do Dashboard.

- Qualidade: Revisão técnica do código Python e validação da integridade dos dados transformados antes da exibição final.

- Análise Visual: Desenvolvimento de gráficos de correlação e mapas de calor para identificar os principais fatores de evasão acadêmica.
   
## 🛠️ 5. Tecnologias Utilizadas:
Para a execução deste projeto, foram selecionadas as seguintes ferramentas:

* **Linguagem:** ![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
* **Manipulação de Dados:** ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=flat&logo=pandas&logoColor=white)
* **Dashboard:** ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)
  
## 📁 6. Estrutura
```
projeto/
├── data/
│   ├── student_dropout_dataset_v3.csv
│   └── base_tratada.csv
├── src/
│   └── etl.py
└── app/
    └── dashboard.py
```
