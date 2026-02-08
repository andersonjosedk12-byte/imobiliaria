# 🏠 Análise de Mercado Imobiliário

Este projeto é um dashboard interativo para análise de dados de mercado imobiliário, focado em aluguel de apartamentos. Desenvolvido com Python, Pandas e Streamlit, permite visualizar e analisar tendências de preços por diferentes critérios como bairro, tamanho do imóvel e outras características.

## 🚀 Funcionalidades

- Visualização de médias de aluguel por bairro
- Análise de preços por tamanho do imóvel
- Filtros interativos para personalizar a análise
- Visualizações gráficas interativas
- Dados formatados no padrão monetário brasileiro (R$)

## 📊 Métricas Principais

- Média de aluguel dos imóveis
- Custo mensal médio
- Preço médio por m²
- Total de ofertas disponíveis

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Pandas
- Streamlit
- Plotly
- NumPy

## 🚀 Como Executar

1. Clone o repositório
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute o dashboard:
   ```
   streamlit run dash.py
   ```
4. Acesse no navegador o endereço indicado no terminal (geralmente http://localhost:8501)

## 📋 Requisitos

- Python 3.8+
- Bibliotecas listadas em `requirements.txt`

## 📊 Estrutura do Projeto

- `dash.py` - Código principal do dashboard
- `dados_apartamentos_limpos.csv` - Base de dados dos imóveis
- `requirements.txt` - Dependências do projeto

## 📈 Visualizações

O dashboard inclui:

1. **Visão Geral** com KPIs principais
2. Gráfico de Média de Aluguel por Bairro
3. Análise de Preço por Tamanho do Imóvel
4. Filtros interativos para personalizar a análise

## 📝 Licença

Este projeto está sob a licença MIT.
