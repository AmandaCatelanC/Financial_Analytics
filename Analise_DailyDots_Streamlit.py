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

O gráfico abaixo mostra a distribuição dos temas e a porcentagem de comentários associados a cada um deles em relação a todos os comentários da base retirando comentários que não foi possível categorizar.
""")

# Agrupar e calcular porcentagem de comentários por tema
comentarios_por_tema = df_explodido.groupby('Temas')['quantidade_comentarios'].sum().sort_values(ascending=False)
comentarios_percentual = (comentarios_por_tema / comentarios_por_tema.sum()) * 100
df_plot = comentarios_percentual.reset_index()
df_plot.columns = ['Temas', 'porcentagem']

# Criar gráfico
fig, ax = plt.subplots(figsize=(8, 4))
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

# 1. Contar quantos de cada engajamento por tema
contagem = df_explodido.groupby(['Temas', 'engajamento']).size().unstack(fill_value=0)

# 2. Calcular porcentagem por linha (por tema)
porcentagem = contagem.div(contagem.sum(axis=1), axis=0) * 100

# 3. Transformar de wide para long
porcentagem_long = porcentagem.reset_index().melt(
    id_vars='Temas', var_name='engajamento', value_name='porcentagem'
)


# --- Paleta personalizada ---
custom_palette = {
    'baixo': '#A7C7E7',   # azul pastel
    'médio': '#FFFACD',   # amarelo pastel
    'alto': '#A8E6CF'     # verde pastel
}

# --- Criar gráfico ---
fig_1, ax = plt.subplots(figsize=(16, 6))
sns.barplot(
    data=porcentagem_long,
    x='Temas',
    y='porcentagem',
    hue='engajamento',
    order=df_explodido['Temas'].value_counts().index,
    palette=custom_palette,
    ax=ax
)

ax.set_title('Distribuição Percentual de Engajamento por Tema')
ax.set_xlabel('Tema')
ax.set_ylabel('Porcentagem (%)')
ax.tick_params(axis='x', rotation=45)
ax.legend(title='Engajamento')

# Rótulos em cada barra
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', label_type='edge', padding=3)

plt.tight_layout()

# --- Mostrar no Streamlit ---
st.pyplot(fig_1)





