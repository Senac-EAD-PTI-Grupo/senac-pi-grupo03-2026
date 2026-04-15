import pandas as pd

# Leitura inicial do dataset
df = pd.read_csv('projeto/data/student_dropout_dataset_v3.csv')

print("Verificando a quantidade de valores vazios por coluna:")
print(df.isnull().sum()) 

# TRATAMENTO DOS DADOS

# 1. LIMPEZA
# O dataset possui alunos sem dados, como Family_Income, Study_Hours_per_Day e Stress_Index
# Vamos preencher esses vazios com a mediana de suas respectivas colunas para não distorcer a análise:
colunas_para_preencher = ['Family_Income', 'Study_Hours_per_Day', 'Stress_Index']
for coluna in colunas_para_preencher: # linha de repetição que vai procurar as colunas vazias em 
    df[coluna] = df[coluna].fillna(df[coluna].median()) #o "fillna" procura as colunas vazias e preenche com a "median"

# 2. CONVERSÃO DE VARIÁVEIS CATEGÓRICAS
# Convertendo textos em números para criação de gráficos posteriores 
# Convertendo respostas 'Yes'/'No' para 1 e 0:
mapeamento_yes_no = {'Yes': 1, 'No': 0}
df['Internet_Access'] = df['Internet_Access'].map(mapeamento_yes_no) # convertendo a coluna de acesso a internet
df['Part_Time_Job'] = df['Part_Time_Job'].map(mapeamento_yes_no) # convertendo a coluna de trabalho meio periodo
df['Scholarship'] = df['Scholarship'].map(mapeamento_yes_no) # convertendo a coluna de bolsa de estudos