import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
INPUT_FILE = DATA_DIR / "student_dropout_dataset_v3.csv"
OUTPUT_FILE = DATA_DIR / "base_tratada.csv"

df = pd.read_csv(INPUT_FILE)

print("Valores nulos por coluna (antes do tratamento):")
print(df.isnull().sum())

# 1. LIMPEZA — preenche nulos numéricos com a mediana
colunas_numericas = ['Family_Income', 'Study_Hours_per_Day', 'Stress_Index']
for coluna in colunas_numericas:
    df[coluna] = df[coluna].fillna(df[coluna].median())

# Preenche nulos categóricos com a moda
df['Parental_Education'] = df['Parental_Education'].fillna(df['Parental_Education'].mode()[0])

# 2. CONVERSÃO DE VARIÁVEIS CATEGÓRICAS — Yes/No → 1/0
mapeamento_yes_no = {'Yes': 1, 'No': 0}
df['Internet_Access'] = df['Internet_Access'].map(mapeamento_yes_no) # convertendo a coluna de acesso a internet
df['Part_Time_Job'] = df['Part_Time_Job'].map(mapeamento_yes_no) # convertendo a coluna de trabalho meio periodo
df['Scholarship'] = df['Scholarship'].map(mapeamento_yes_no) # convertendo a coluna de bolsa de estudos

print("\nValores nulos por coluna (após tratamento):")
print(df.isnull().sum())
print(f"\nBase tratada salva em: {OUTPUT_FILE}")

df.to_csv(OUTPUT_FILE, index=False)
