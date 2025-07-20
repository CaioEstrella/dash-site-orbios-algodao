import pandas as pd
import numpy as np

# Criar dados de exemplo para produção de algodão no Brasil
# Baseado em dados reais da CONAB e IBGE

estados_brasil = [
    'Mato Grosso', 'Bahia', 'Goiás', 'Mato Grosso do Sul', 'Maranhão',
    'Piauí', 'Ceará', 'Minas Gerais', 'São Paulo', 'Paraná',
    'Tocantins', 'Pará', 'Alagoas', 'Paraíba', 'Rio Grande do Norte',
    'Pernambuco', 'Sergipe', 'Rondônia', 'Distrito Federal'
]

# Mapear estados para regiões
regioes_map = {
    'Mato Grosso': 'Centro-Oeste', 'Bahia': 'Nordeste', 'Goiás': 'Centro-Oeste',
    'Mato Grosso do Sul': 'Centro-Oeste', 'Maranhão': 'Nordeste', 'Piauí': 'Nordeste',
    'Ceará': 'Nordeste', 'Minas Gerais': 'Sudeste', 'São Paulo': 'Sudeste',
    'Paraná': 'Sul', 'Tocantins': 'Norte', 'Pará': 'Norte',
    'Alagoas': 'Nordeste', 'Paraíba': 'Nordeste', 'Rio Grande do Norte': 'Nordeste',
    'Pernambuco': 'Nordeste', 'Sergipe': 'Nordeste', 'Rondônia': 'Norte',
    'Distrito Federal': 'Centro-Oeste'
}

# Mapear siglas dos estados
siglas_map = {
    'Mato Grosso': 'MT', 'Bahia': 'BA', 'Goiás': 'GO', 'Mato Grosso do Sul': 'MS',
    'Maranhão': 'MA', 'Piauí': 'PI', 'Ceará': 'CE', 'Minas Gerais': 'MG',
    'São Paulo': 'SP', 'Paraná': 'PR', 'Tocantins': 'TO', 'Pará': 'PA',
    'Alagoas': 'AL', 'Paraíba': 'PB', 'Rio Grande do Norte': 'RN',
    'Pernambuco': 'PE', 'Sergipe': 'SE', 'Rondônia': 'RO', 'Distrito Federal': 'DF'
}

# Gerar dados históricos de 2000 a 2024
anos = list(range(2000, 2025))

# Dados base de produção (em toneladas) - baseado em padrões reais
producao_base = {
    'Mato Grosso': 2500000,  # Maior produtor
    'Bahia': 1200000,
    'Goiás': 600000,
    'Mato Grosso do Sul': 400000,
    'Maranhão': 300000,
    'Piauí': 200000,
    'Ceará': 150000,
    'Minas Gerais': 100000,
    'São Paulo': 80000,
    'Paraná': 60000,
    'Tocantins': 40000,
    'Pará': 30000,
    'Alagoas': 20000,
    'Paraíba': 15000,
    'Rio Grande do Norte': 10000,
    'Pernambuco': 8000,
    'Sergipe': 5000,
    'Rondônia': 3000,
    'Distrito Federal': 2000
}

# Criar dataset
data = []

for ano in anos:
    for estado in estados_brasil:
        # Adicionar tendência e variação aleatória
        crescimento_anual = 0.03 if ano > 2005 else -0.02  # Crescimento após modernização
        variacao = np.random.normal(1, 0.15)  # Variação climática/econômica
        
        # Cálculo da produção com base no ano
        producao = producao_base[estado] * (1 + crescimento_anual * (ano - 2000)) * variacao
        producao = max(0, int(producao))  # Não pode ser negativa
        
        data.append({
            'ano': ano,
            'estado': estado,
            'sigla': siglas_map[estado],
            'regiao': regioes_map[estado],
            'producao': producao
        })

# Criar DataFrame
df = pd.DataFrame(data)

# Exibir preview dos dados
print("Dados criados - Preview:")
print(df.head(10))
print(f"\nTotal de registros: {len(df)}")
print(f"Anos: {df['ano'].min()} - {df['ano'].max()}")
print(f"Estados: {df['estado'].nunique()}")
print("\nProdução por região (últimos dados - 2024):")
print(df[df['ano'] == 2024].groupby('regiao')['producao'].sum().sort_values(ascending=False))

# Salvar dados
df.to_csv('dados_algodao.csv', index=False)
print("\nDados salvos em: dados_algodao.csv")