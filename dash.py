import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuração da página
st.set_page_config(page_title='🏠 Análise de Mercado Imobiliário', layout='wide')

import os

# Obter o diretório atual do script
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'dados_apartamentos_limpos.csv')

# Carregar dados
@st.cache_data
def load_data():
    return pd.read_csv(csv_path, sep=';', encoding='utf-8')

df = load_data()

# Título e descrição
st.title('🏠 Análise de Mercado Imobiliário')
st.markdown("""
### Encontre o apartamento ideal para o seu perfil e orçamento
Explore os dados de aluguel de apartamentos e encontre as melhores oportunidades no mercado.
""")

# ===== BARRA LATERAL DE FILTROS =====
st.sidebar.header('Filtros')

# Filtro de Bairros
bairros = st.sidebar.multiselect(
    'Selecione os Bairros',
    options=sorted(df['Bairro'].unique()),
    default=[]
)

# Função para formatar valores em Real
def format_brl(valor):
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

# Filtro de Faixa de Preço
st.sidebar.markdown('**Faixa de Preço (R$)**')
min_val, max_val = float(df['Valor'].min()), float(df['Valor'].max())

# Criar colunas para os campos de entrada
col1, col2 = st.sidebar.columns(2)

with col1:
    min_valor = st.number_input(
        'Mínimo',
        min_value=0.0,
        max_value=float(df['Valor'].max()),
        value=float(df['Valor'].min()),
        step=100.0
    )

with col2:
    max_valor = st.number_input(
        'Máximo',
        min_value=0.0,
        max_value=float(df['Valor'].max()),
        value=float(df['Valor'].max()),
        step=100.0
    )

# Garantir que o valor mínimo não seja maior que o máximo
if min_valor > max_valor:
    st.sidebar.warning('O valor mínimo não pode ser maior que o máximo.')
    min_valor = max_valor - 1  # Ajuste para um valor válido

st.sidebar.markdown("---")

# Filtro de Número de Quartos
quartos = st.sidebar.multiselect(
    'Nº de Quartos',
    options=sorted(df['Quartos'].unique()),
    default=sorted(df['Quartos'].unique())
)

# Filtro de Suíte (usando a coluna 'Suites' que contém 0 ou 1)
possui_suite = st.sidebar.radio(
    'Possui Suíte?',
    options=['Todos', 'Sim', 'Não'],
    index=0
)

# Filtro de Vagas de Garagem
vagas = st.sidebar.multiselect(
    'Vagas de Garagem',
    options=sorted(df['Vagas'].unique()),
    default=sorted(df['Vagas'].unique())
)

# Aplicar filtros
df_filtered = df.copy()

if bairros:
    df_filtered = df_filtered[df_filtered['Bairro'].isin(bairros)]

if quartos:
    df_filtered = df_filtered[df_filtered['Quartos'].isin(quartos)]

if possui_suite != 'Todos':
    df_filtered = df_filtered[df_filtered['Suites'] == (1 if possui_suite == 'Sim' else 0)]

if vagas:
    df_filtered = df_filtered[df_filtered['Vagas'].isin(vagas)]

df_filtered = df_filtered[
    (df_filtered['Valor'] >= min_valor) & 
    (df_filtered['Valor'] <= max_valor)
]

# ===== KPI CARDS =====
st.markdown('---')
st.subheader('Visão Geral')

if not df_filtered.empty:
    # Calcular métricas
    media_aluguel = df_filtered['Valor'].mean()
    media_custo_mensal = df_filtered['Valor_por_mes'].mean()
    preco_medio_m2 = (df_filtered['Valor'].sum() / df_filtered['Area'].sum()) if df_filtered['Area'].sum() > 0 else 0
    total_ofertas = len(df_filtered)
    
    # Função para formatar valores em Real
    def format_brl(valor):
        if pd.isna(valor):
            return 'R$ 0,00'
        return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    
    # Exibir KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Média de Aluguel", format_brl(media_aluguel))
    with col2:
        st.metric("Custo Mensal Médio", format_brl(media_custo_mensal))
    with col3:
        st.metric("Preço Médio por m²", format_brl(preco_medio_m2))
    with col4:
        st.metric("Total de Ofertas", f"{total_ofertas:,.0f}".replace('.', ','))

    # ===== VISUALIZAÇÕES =====
    st.markdown('---')
    
    # Gráfico 1: Ranking de Bairros (Simplificado)
    st.subheader('Média de Aluguel por Bairro')
    if len(df_filtered['Bairro'].unique()) > 1:
        bairros_media = df_filtered.groupby('Bairro')['Valor'].mean().sort_values().tail(10)  # Top 10 bairros
        
        # Criar formatação personalizada para os textos das barras
        text_values = [f'R$ {x:,.2f}'.replace('.', 'X').replace(',', '.').replace('X', ',') 
                      for x in bairros_media.values]
        
        fig1 = px.bar(
            bairros_media, 
            orientation='h',
            color=bairros_media.values,
            color_continuous_scale='blues',
            labels={'value': 'Média de Aluguel (R$)', 'index': 'Bairro'},
            text=text_values
        )
        
        # Melhorar formatação
        fig1.update_layout(
            showlegend=False,
            yaxis_title='',
            xaxis_title='Média de Aluguel',
            height=400
        )
        
        # Formatar eixo X no padrão monetário brasileiro
        fig1.update_xaxes(
            tickprefix='R$ ',
            tickformat='.,2f',
            ticktext=[f'R$ {x:,.2f}'.replace('.', 'X').replace(',', '.').replace('X', ',') 
                     for x in bairros_media.values]
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info('Selecione mais de um bairro para ver o ranking.')
    
    # Gráfico 2: Média de Preço por Tamanho do Imóvel
    st.subheader('Média de Preço por Tamanho do Imóvel')
    
    # Criar categorias de tamanho
    df_filtered['Faixa de Tamanho'] = pd.cut(
        df_filtered['Area'],
        bins=[0, 50, 70, 90, 120, float('inf')],
        labels=['Até 50m²', '51-70m²', '71-90m²', '91-120m²', 'Acima de 120m²']
    )
    
    # Calcular médias
    media_por_tamanho = df_filtered.groupby('Faixa de Tamanho')['Valor'].mean().reset_index()
    
    # Criar formatação personalizada para os textos das barras
    text_values = [f'R$ {x:,.2f}'.replace('.', 'X').replace(',', '.').replace('X', ',') 
                  for x in media_por_tamanho['Valor']]
    
    # Criar gráfico de barras horizontais
    fig2 = px.bar(
        media_por_tamanho,
        x='Valor',
        y='Faixa de Tamanho',
        orientation='h',
        text=text_values,
        color='Faixa de Tamanho',
        color_discrete_sequence=px.colors.sequential.Blues_r,
        labels={'Valor': 'Média de Aluguel (R$)', 'Faixa de Tamanho': 'Tamanho do Imóvel'}
    )
    
    # Melhorar formatação
    fig2.update_layout(
        showlegend=False,
        yaxis_title='',
        xaxis_title='Média de Aluguel',
        height=400,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    
    # Formatar eixo X no padrão monetário brasileiro
    fig2.update_xaxes(
        tickprefix='R$ ',
        tickformat='.,2f',
        ticktext=[f'R$ {x:,.2f}'.replace('.', 'X').replace(',', '.').replace('X', ',') 
                 for x in fig2.data[0].x]
    )
    fig2.update_layout(
        xaxis_title='Média de Aluguel'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Adicionar tabela com contagem de imóveis por faixa
    contagem_por_tamanho = df_filtered['Faixa de Tamanho'].value_counts().sort_index()
    
    st.markdown('**Quantidade de imóveis por faixa de tamanho:**')
    st.dataframe(
        contagem_por_tamanho.rename('Quantidade de Imóveis'),
        use_container_width=True
    )
    
    # Gráfico 3: Distribuição de Preços (Simplificada)
    st.subheader('Distribuição de Preços')
    
    # Criar faixas de preço
    bins = [0, 1000, 2000, 3000, 4000, 5000, float('inf')]
    labels = ['Até R$1.000', 'R$1.001-2.000', 'R$2.001-3.000', 'R$3.001-4.000', 'R$4.001-5.000', 'Acima de R$5.000']
    
    df_filtered['Faixa_Preco'] = pd.cut(df_filtered['Valor'], bins=bins, labels=labels)
    contagem = df_filtered['Faixa_Preco'].value_counts().sort_index()
    
    fig3 = px.bar(
        x=contagem.index,
        y=contagem.values,
        text=contagem.values,
        color=contagem.index,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    
    # Melhorar formatação
    fig3.update_layout(
        showlegend=False,
        xaxis_title='Faixa de Preço',
        yaxis_title='Número de Imóveis',
        height=400
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Gráfico 4: Comparação com/sem Suíte (Simplificado)
    st.subheader('Média de Aluguel: Com vs Sem Suíte')
    
    if 'Suites' in df_filtered.columns and len(df_filtered['Suites'].unique()) > 1:
        # Calcular médias
        media_com_suite = df_filtered[df_filtered['Suites'] == 1]['Valor'].mean()
        media_sem_suite = df_filtered[df_filtered['Suites'] == 0]['Valor'].mean()
        
        # Criar DataFrame para o gráfico
        dados = pd.DataFrame({
            'Tipo': ['Com Suíte', 'Sem Suíte'],
            'Média de Aluguel': [media_com_suite, media_sem_suite]
        })
        
        fig4 = px.bar(
            dados,
            x='Tipo',
            y='Média de Aluguel',
            color='Tipo',
            text_auto='.2f',
            color_discrete_sequence=['#1f77b4', '#ff7f0e']
        )
        
        # Melhorar formatação
        fig4.update_layout(
            showlegend=False,
            xaxis_title='',
            yaxis_title='Média de Aluguel (R$)',
            height=400
        )
        
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info('Selecione imóveis com e sem suíte para ver a comparação.')
    
    # Tabela com os dados
    st.subheader('Dados Detalhados')
    st.dataframe(
        df_filtered[['Bairro', 'Quartos', 'Vagas', 'Area', 'Valor', 'Condominio', 'Valor_por_mes']].sort_values('Valor'),
        column_config={
            'Bairro': 'Bairro',
            'Quartos': 'Quartos',
            'Vagas': 'Vagas',
            'Area': 'Área (m²)',
            'Valor': 'Aluguel (R$)',
            'Condominio': 'Condomínio (R$)',
            'Valor_por_mes': 'Custo Total (R$)'
        },
        use_container_width=True
    )
    
    # Botão para baixar os dados filtrados
    csv = df_filtered.to_csv(index=False, sep=';', decimal=',').encode('utf-8')
    st.download_button(
        label='Baixar Dados Filtrados (CSV)',
        data=csv,
        file_name='dados_filtrados.csv',
        mime='text/csv'
    )
else:
    st.warning('Nenhum imóvel encontrado com os filtros selecionados. Tente ajustar os critérios de busca.')

# Rodapé
st.markdown('---')
st.markdown('*Dados atualizados em ' + pd.Timestamp.now().strftime('%d/%m/%Y %H:%M') + '*')