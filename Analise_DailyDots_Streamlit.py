# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Ativar layout wide (tela cheia)
st.set_page_config(layout="wide")

# Reduzir margens laterais com CSS
st.markdown("""
    <style>
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

# Título centralizado
st.markdown(
    "<h1 style='text-align: center; white-space: nowrap;'>Análise de Engajamento no DailyDots</h1>", 
    unsafe_allow_html=True
)

# Ler o CSV
df_explodido = pd.read_csv("tabela_tratada_base_exemplo.csv", encoding="utf-8-sig")

# Exibir preview da base
st.write("### Preview das 3 primeiras linhas da tabela")	
st.dataframe(df_explodido.head(3))  # tabela interativa

# Corrigido aqui para df_explodido
st.metric(label="Total de registros", value=f"{len(df_explodido):,}")

# Texto explicativo (storytelling)
st.markdown("""
Este conjunto de dados foi coletado por meio de um **chatbot com IA via WhatsApp**, onde usuários interagem com o app **DailyDots**, um diário digital focado em **autoconhecimento e saúde emocional**. As interações são classificadas em tipos como *Journaling*, *Desabafo*, *Reflexão Profunda* e *Reflexão Curta", como registrado na coluna `Tipo`.

Todos os dados respeitam a **LGPD** — os usuários foram anonimizados (`user_id`), e nenhum dado sensível foi exposto.

Colunas importantes da base:
- `Tipo`: tipo de escrita do usuário.
- `Vibe`: tom emocional (positiva, negativa ou neutra).
- `Temas` e `Subtemas`: tópicos extraídos do texto.
- `quantidade_comentarios`, `engajamento` e `tema`: colunas criadas por meio de **engenharia de atributos**, ou comumente chamado de engenharia de features.
""")

st.markdown("### Dicionário de Variáveis")

st.markdown("""
<div style='display: flex; justify-content: center'>
  <table style='border-collapse: collapse; width: 90%; text-align: left;'>
    <thead>
      <tr>
        <th style='border: 1px solid #ccc; padding: 8px;'>Coluna</th>
        <th style='border: 1px solid #ccc; padding: 8px;'>Descrição</th>
      </tr>
    </thead>
    <tbody>
      <tr><td style='border: 1px solid #ccc; padding: 8px;'>user_id</td><td style='border: 1px solid #ccc; padding: 8px;'>Identificador anonimizado do usuário.</td></tr>
      <tr><td style='border: 1px solid #ccc; padding: 8px;'>data</td><td style='border: 1px solid #ccc; padding: 8px;'>Data da entrada no DailyDots.</td></tr>
      <tr><td style='border: 1px solid #ccc; padding: 8px;'>Tipo</td><td style='border: 1px solid #ccc; padding: 8px;'>Tipo da escrita (Journaling, Desabafo etc.).</td></tr>
      <tr><td style='border: 1px solid #ccc; padding: 8px;'>Reflexoes</td><td style='border: 1px solid #ccc; padding: 8px;'>Indica se houve reflexão no texto.</td></tr>
      <tr><td style='border: 1px solid #ccc; padding: 8px;'>Pensamento Suicida</td><td style='border: 1px solid #ccc; padding: 8px;'>Indica se o conteúdo traz menções a pensamentos suicidas.</td></tr>
      <tr><td style='border: 1px solid #ccc; padding: 8px;'>Elogio</td><td style='border: 1px solid #ccc; padding: 8px;'>Se o usuário elogiou o app ou a experiência.</td></tr>
      <tr><td style='border: 1px solid #ccc; padding: 8px;'>Sugestoes da IA</td><td style='border: 1px solid #ccc; padding: 8px;'>Se a IA fez sugestões automáticas ao usuário.</td></tr>
      <tr><td style='border: 1px solid #ccc; padding: 8px;'>Tamanho</td><td style='border: 1px solid #ccc; padding: 8px;'>Comprimento do texto (Muito curto, Normal etc.).</td></tr>
      <tr><td style='border: 1px solid #ccc; padding: 8px;'>Vibe</td><td style='border: 1px solid #ccc; padding: 8px;'>Tom emocional da mensagem (Positiva, Neutra, Negativa).</td></tr>
      <tr><td style='border: 1px solid #ccc; padding: 8px;'>Temas</td><td style='border: 1px solid #ccc; padding: 8px;'>Tema principal extraído do conteúdo.</td></tr>
      <tr><td style='border: 1px solid #ccc; padding: 8px;'>Subtemas</td><td style='border: 1px solid #ccc; padding: 8px;'>Subtemas identificados no texto.</td></tr>
      <tr><td style='border: 1px solid #ccc; padding: 8px;'>quantidade_comentarios</td><td style='border: 1px solid #ccc; padding: 8px;'><b>Feature criada</b> que indica o número de comentários recebidos.</td></tr>
      <tr><td style='border: 1px solid #ccc; padding: 8px;'>engajamento</td><td style='border: 1px solid #ccc; padding: 8px;'><b>Feature criada</b> que classifica o nível de engajamento (baixo, médio, alto).</td></tr>
      <tr><td style='border: 1px solid #ccc; padding: 8px;'>tema</td><td style='border: 1px solid #ccc; padding: 8px;'><b>Feature tratada</b>, extraída e categorizada a partir de Temas e Subtemas.</td></tr>
    </tbody>
  </table>
</div>
""", unsafe_allow_html=True)

st.markdown("""
A partir dos temas, foi criado pela autora uma categorização em blocos como **Familiar, Amoroso, Saúde, Rotina, Depressão, Acadêmicos, Financeiros, etc.** com o objetivo de **entender o que influencia o engajamento dos usuários** com o app.

O gráfico abaixo mostra a distribuição dos temas e a porcentagem de comentários associados a cada um deles em relação a todos os comentários da base.
""")

# Primeiro Gráfico ----------------------------------------------------------------------------------------------------------------------------
# Agrupar e calcular porcentagem de comentários por tema
comentarios_por_tema = df_explodido.groupby('Temas')['quantidade_comentarios'].sum().sort_values(ascending=False)
comentarios_percentual = (comentarios_por_tema / comentarios_por_tema.sum()) * 100
df_plot = comentarios_percentual.reset_index()
df_plot.columns = ['Temas', 'porcentagem']

# Criar gráfico
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(
    data=df_plot,
    x='Temas',
    y='porcentagem',
    order=df_plot['Temas'],
    color='skyblue',
    ax=ax
)

# Adicionar rótulos em %
for i, p in enumerate(ax.patches):
    valor = df_plot['porcentagem'].iloc[i]
    ax.annotate(f'{valor:.1f}%', 
                (p.get_x() + p.get_width() / 2, p.get_height()), 
                ha='center', va='bottom', fontsize=10)

ax.set_title(u'Distribuição Percentual de Comentários por Tema')
ax.set_xlabel('Tema')
ax.set_ylabel('Porcentagem (%)')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()

# Mostrar no Streamlit
st.pyplot(fig)

st.markdown("""
Podemos observar que as pessoas costumam abordar com frequência temas como **Família**, **Trabalho**, **Relacionamentos Amorosos** e **Rotina**.  
Esses assuntos se destacam e podem representar boas oportunidades como **chamadas para campanhas publicitárias futuras**.

Agora, considerando essa divisão temática, é interessante observarmos **quais temas geram mais engajamento**.  
Em outras palavras, quais tópicos fazem as pessoas se envolverem mais e escreverem com maior frequência?

""")

# Segundo Gráfico --------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------

# 1. Contar quantos de cada engajamento por tema
contagem = df_explodido.groupby(['Temas', 'engajamento']).size().unstack(fill_value=0)

# 2. Calcular porcentagem por linha (por tema)
porcentagem = contagem.div(contagem.sum(axis=1), axis=0) * 100

# 3. Transformar de wide para long
porcentagem_long = porcentagem.reset_index().melt(
    id_vars='Temas', var_name='engajamento', value_name='porcentagem'
)

# Padronizar os nomes da coluna de engajamento (caso haja variação)
porcentagem_long['engajamento'] = porcentagem_long['engajamento'].str.capitalize()

# Paleta personalizada
custom_palette = {
    'Baixo': '#F08080',
    'Médio': '#FFFACD',
    'Alto': '#A8E6CF'
}

# Criar gráfico
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(
    data=porcentagem_long,
    x='Temas',
    y='porcentagem',
    hue='engajamento',
    order=df_explodido['Temas'].value_counts().index,
    palette=custom_palette,
    ax=ax
)

# Adicionar rótulos com os containers do seaborn
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', label_type='edge', padding=3, fontsize=9)

# Ajustes finais
ax.set_title('Distribuição Percentual de Engajamento por Tema')
ax.set_xlabel('Temas')
ax.set_ylabel('Porcentagem (%)')
ax.legend(title='Engajamento')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()

# Exibir no Streamlit
st.pyplot(fig)

st.markdown("""
---
O gráfico mostra o **percentual de engajamento por tema**, revelando que temas como **Família**, **Trabalho**, **Rotina** e **Saúde** apresentam **mais de 70% de engajamento alto**.

A partir disso, surge uma pergunta: **qual é o tipo de vibe associado a esses temas mais engajadores**, como Família, Trabalho e Rotina?  
Será que são acompanhados por sentimentos mais positivos, negativos ou neutros?

Os gráficos a seguir nos ajudam a visualizar essa relação:
""")
# ------------------------------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Paletas
custom_palette = {
    'baixo': '#F08080',   # vermelho claro (ajustei o comentário)
    'médio': '#FFFACD',   # amarelo pastel
    'alto': '#A8E6CF'     # verde pastel
}

vibe_palette = {
    'Muito Negativa': '#FFB6B6',
    'Negativa': '#FFA07A',
    'Neutra': '#FFFACD',
    'Positiva': '#A8E6CF',
    'Muito Positiva': '#A7C7E7'
}

# --- Gráfico 1: Vibe por Nível de Engajamento ---

# 1. Contagem por 'Vibe' e 'engajamento'
contagem_Vibe = df_explodido.groupby(['Vibe', 'engajamento']).size().unstack(fill_value=0)

# 2. Porcentagem por linha
porcentagem_Vibe = contagem_Vibe.div(contagem_Vibe.sum(axis=1), axis=0) * 100

# 3. De wide para long
porcentagem_long_1 = porcentagem_Vibe.reset_index().melt(
    id_vars='Vibe', var_name='engajamento', value_name='porcentagem_Vibe'
)

# Ordenar 'Vibe' pela frequência na base original
ordem_vibe = df_explodido['Vibe'].value_counts().index.tolist()

fig1, ax1 = plt.subplots(figsize=(14, 10))
sns.barplot(
    data=porcentagem_long_1,
    x='Vibe',
    y='porcentagem_Vibe',
    hue='engajamento',
    palette=custom_palette,
    order=ordem_vibe,
    ax=ax1
)

ax1.set_title('Vibe por Nível de Engajamento')
ax1.set_xlabel('Vibe')
ax1.set_ylabel('Porcentagem (%)')
ax1.tick_params(axis='x', rotation=45)
ax1.legend(title='Engajamento')

for container in ax1.containers:
    ax1.bar_label(container, fmt='%.1f%%', label_type='edge', padding=3)

plt.tight_layout()


# --- Gráfico 2: Distribuição de Pessoas por Vibe ---

contagem_vibe = df_explodido['Vibe'].value_counts()
porcentagem_vibe = (contagem_vibe / contagem_vibe.sum()) * 100

df_vibe = pd.DataFrame({
    'Vibe': contagem_vibe.index,
    'quantidade': contagem_vibe.values,
    'porcentagem': porcentagem_vibe.values
})

# Ordem desejada para o gráfico 2
ordem = ['Muito Negativa', 'Negativa', 'Neutra', 'Positiva', 'Muito Positiva']
df_vibe = df_vibe.set_index('Vibe').reindex(ordem).reset_index()

fig2, ax2 = plt.subplots(figsize=(14, 10))
sns.barplot(
    data=df_vibe,
    x='Vibe',
    y='quantidade',
    palette=vibe_palette,
    order=ordem,

)

for i, row in df_vibe.iterrows():
    ax2.text(
        i,
        row['quantidade'] + max(df_vibe['quantidade']) * 0.01,
        f"{int(row['quantidade'])} ({row['porcentagem']:.1f}%)",
        ha='center',
        va='bottom',
        fontsize=10
    )

ax2.set_title("Distribuição de Pessoas por Vibe")
ax2.set_xlabel("Vibe")
ax2.set_ylabel("Quantidade de Pessoas")
ax2.tick_params(axis='x', rotation=30)

plt.tight_layout()

# --- Exibir lado a lado no Streamlit ---

col1, col2 = st.columns(2)

with col1:
    st.pyplot(fig1)

with col2:
    st.pyplot(fig2)


# Gráfico ------------------------------------------------------------------------------------------------------------------------------------

st.markdown("""
Podemos notar que **vibes mais positivas tendem a ter maior engajamento**.  
Além disso, a **vibe neutra** é a mais frequentemente registrada nas entradas da base, mostrando equilíbrio no tom geral das reflexões.

---

Também é possível investigar se o **tipo de reflexão** influencia o engajamento.  
O gráfico abaixo indica que pessoas com **nível de engajamento mais alto** tendem a escrever **reflexões mais profundas**.
""")

# Gráfico ------------------------------------------------------------------------------------------------------------------------------------

# 1. Contagem por 'Reflexoes' e 'engajamento'
contagem_Reflexoes = df_explodido.groupby(['Reflexoes', 'engajamento']).size().unstack(fill_value=0)

# 2. Porcentagem por linha
porcentagem_Reflexoes = contagem_Reflexoes.div(contagem_Reflexoes.sum(axis=1), axis=0) * 100

# 3. De wide para long
porcentagem_long_3 = porcentagem_Reflexoes.reset_index().melt(
    id_vars='Reflexoes', var_name='engajamento', value_name='porcentagem_Reflexoes'
)

# Ordenar 'Reflexoes' pela frequência na base original
ordem_Reflexoes = df_explodido['Reflexoes'].value_counts().index.tolist()

fig3, ax1 = plt.subplots(figsize=(14, 10))
sns.barplot(
    data=porcentagem_long_3,
    x='Reflexoes',
    y='porcentagem_Reflexoes',
    hue='engajamento',
    palette=custom_palette,
    order=ordem_Reflexoes,
    ax=ax1
)

ax1.set_title('Tipo de Reflexão por Nível de Engajamento')
ax1.set_xlabel('Reflexão')
ax1.set_ylabel('Porcentagem (%)')
ax1.tick_params(axis='x', rotation=45)
ax1.legend(title='Engajamento')

for container in ax1.containers:
    ax1.bar_label(container, fmt='%.1f%%', label_type='edge', padding=3)

plt.tight_layout()

st.pyplot(fig3)

# --------------------------------------------------- Tabela Regressão -----------------------------------------------------------------

st.markdown("**Relatório de Classificação:**")
st.markdown("""
Com uma acurácia de **0.65**, observamos que os fatores que mais impulsionam o engajamento no uso do *DailyDots* estão relacionados a uma **vibe mais positiva** nas mensagens, além de **temas como Família, Rotina e Saúde**, que se destacam entre os mais engajadores.

Outro ponto importante é que **reflexões mais profundas** também estão associadas a níveis mais altos de interação com a plataforma.

Com base nesses insights, uma sugestão estratégica seria adaptar o comportamento do modelo de linguagem (*LLM*) para:

- Estimular conversas em torno desses temas;
- Promover uma atmosfera mais positiva;
- Encorajar reflexões mais significativas por meio de perguntas com maior profundidade.

Essa abordagem pode contribuir diretamente para o aumento do engajamento dos usuários com o *DailyDots*.
""")


# ⬇️ Tabela: Top variáveis associadas ao engajamento alto
st.markdown("**Top variáveis mais associadas ao engajamento alto:**")

import pandas as pd

top_variaveis = pd.DataFrame({
    "Alto": [0.703, 0.692, 0.570, 0.427, 0.422, 0.406, 0.388, 0.351, 0.345, 0.344,
             0.325, 0.291, 0.190],
    "Baixo": [0.020, -0.597, -0.087, 0.150, 0.097, -0.092, -0.246, -0.388, -0.341,
              -0.394, -0.514, -0.295, -0.014],
    "Médio": [-0.723, -0.095, -0.483, -0.577, -0.519, -0.314, -0.142, 0.037, -0.004,
              0.050, 0.188, 0.004, -0.176]
}, index=[
    "Vibe_Muito Positiva",
    "tema_Saúde",
    "Temas_Autoconhecimento",
    "Tipo_Reflexão Profunda",
    "tema_Depressão",
    "tema_Amizade",
    "tema_Familiar",
    "Vibe_Positiva",
    "Temas_Familiar",
    "tema_Rotina",
    "Temas_Uso Aplicativo",
    "Temas_Trabalho",
    "Vibe_Neutra"
])

st.dataframe(top_variaveis.round(3).style.format("{:.3f}").set_caption("Coeficientes por classe"))


