# 📋 Plano de Ação - Melhorias do Dashboard (Grupo 03)

Este documento centraliza as próximas tarefas sugeridas para elevar o nível do nosso painel no Streamlit, transformando-o em uma ferramenta de Business Intelligence mais profissional, dinâmica e voltada para a tomada de decisão.

## 1. 🎛️ Novos Filtros na Sidebar
Nosso objetivo aqui é permitir que o usuário interaja e "fatie" os dados por características socioeconômicas e acadêmicas, validando hipóteses dinamicamente.

- [ ] **Bolsa de Estudos (`Scholarship`)**: 
  - *Como fazer:* Adicionar um `st.sidebar.radio` (Opções: Todos, Sim, Não) ou checkbox. 
  - *Por quê:* Analisar se ter bolsa reduz os impactos financeiros, o estresse e, consequentemente, a evasão.
- [ ] **Escolaridade dos Pais (`Parental_Education`)**:
  - *Como fazer:* Utilizar um `st.sidebar.multiselect` para as categorias (High School, Bachelor, Master, PhD).
  - *Por quê:* Avaliar a correlação entre o background familiar acadêmico e as taxas de sucesso/retenção dos alunos.
- [ ] **Gênero (`Gender`)**:
  - *Como fazer:* Adicionar um seletor (dropdown ou botões).
  - *Por quê:* Visualizar se a evasão ou o nível de estresse afetam mais um gênero específico em determinados departamentos.
- [ ] **Renda Familiar (`Family_Income`)**:
  - *Como fazer:* Adicionar um `st.sidebar.slider` semelhante ao que já existe para a idade.
  - *Por quê:* Entender se as taxas de evasão flutuam conforme a faixa de renda total da família.

---

## 2. 📝 Contextualização e Conclusões por Seção
Em vez de jogar todas as respostas no início, vamos guiar o usuário através de uma narrativa analítica (storytelling com dados).

- [ ] **Adicionar um Breve Contexto no Topo do Dashboard**:
  - *Como fazer:* Usar blocos de texto (`st.markdown` ou `st.write`) logo abaixo do título para explicar resumidamente do que se trata o projeto e a origem/objetivo da base de dados.
  - *Por quê:* Ajuda a situar o avaliador (ou qualquer outro usuário) sobre o propósito daquele painel antes de mergulhar nos números.
- [ ] **Inserir Conclusões ao Final de Cada Bloco/Aba**:
  - *Como fazer:* Assim como foi feito na seção "Impacto do Trabalho", utilizar `st.info` ou `st.warning` logo abaixo dos gráficos de cada tema (Notas, Perfis, Departamentos) trazendo uma frase que resuma a descoberta.
  - *Por quê:* O usuário absorve muito melhor o insight se a conclusão estiver atrelada visualmente ao gráfico que a originou, tornando a experiência mais modular.

---

## 3. 🎯 Destaque para o Fator Principal (Desempenho / GPA)
De acordo com os relatórios gerados no notebook, as notas são o fator mais definidor da evasão.

- [ ] **Criar Seção de Notas (GPA / CGPA) vs Retenção e Estresse**:
  - *Como fazer:* 
    1. Criar um gráfico comparativo das médias de notas (CGPA) classificadas pelo nível de estresse: 'Estresse > 6', 'Estresse <= 6' e 'Média Geral'.
    2. Logo em seguida, montar uma comparação (cards ou gráfico) da média do CGPA exclusivamente entre os alunos que *desistiram* versus os alunos que *permanecem estudando*.
    3. *Dica:* Esses cálculos e a lógica com as variáveis já estão modelados e validados no `notebooks/exploratory_analysis.ipynb` (na seção sobre "Qual a média do CGPA... com nível de estresse acima de 6?").
  - *Por quê:* É o nosso achado analítico mais forte. Existe uma possível relação ou "efeito cascata": o estresse alto colabora para um CGPA menor, e ambos em conjunto aumentam a probabilidade de evasão. Mostrar essa história de forma sequencial no painel vai gerar um alerta crucial.

---

## 4. 🗂️ Reestruturação de UX: Abas (Extra)
O dashboard está ficando longo com as análises de todos os membros. Vamos organizar.

- [ ] **Dividir o Dashboard utilizando `st.tabs`**:
  - *Como fazer:* Agrupar os gráficos existentes usando `aba1, aba2, aba3 = st.tabs(["📊 Visão Geral", "📚 Engajamento e Desempenho", "🧠 Socioeconômico e Saúde"])`.
  - *Estrutura sugerida:*
    - **Visão Geral:** Métricas principais (cards do topo), Evasão por Semestre e Evasão por Departamento.
    - **Engajamento e Desempenho:** Presença Média, Análise de Notas (vide item 3), Painel de Idades.
    - **Socioeconômico e Saúde:** Impacto do Trabalho (estresse), Gráficos de Correlação (estresse alto vs CGPA), e impacto da renda.
  - *Por quê:* Evita o _scroll infinito_ na página, categoriza bem o trabalho de cada membro da equipe e melhora muito a usabilidade geral (UX).