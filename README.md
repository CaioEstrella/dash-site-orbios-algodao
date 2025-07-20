[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)


# 🌱 Dashboard Produção de Algodão - Brasil

Dashboard interativo desenvolvido em Python com Plotly Dash para análise da produção histórica de algodão no Brasil por estados e regiões.

## 📋 Funcionalidades

### 🗺️ Visualizações Principais
- **Mapa de Calor do Brasil**: Mapa interativo com estados coloridos conforme a produção
- **Série Temporal**: Evolução da produção nacional ao longo dos anos
- **Top 10 Estados**: Ranking dos maiores produtores por período
- **Distribuição Regional**: Gráfico de pizza mostrando participação por região
- **Tabela Detalhada**: Dados completos filtrados e ordenáveis

### 🎛️ Filtros Interativos
- **Range de Anos**: Seleção de período específico com slider
- **Filtro por Região**: Seleção múltipla de regiões brasileiras
- **Filtro por Estado**: Seleção múltipla de estados específicos
- **Ordenação**: Ordenar dados por produção, estado ou região

### 🎨 Interface e Design
- **Modo Escuro/Claro**: Toggle para alternar entre temas
- **Design Responsivo**: Adaptável a diferentes tamanhos de tela
- **Cards de Métricas**: Indicadores principais (produção total, média, líder, crescimento)
- **Interface Moderna**: Baseada em Bootstrap com ícones e cores profissionais

## 🚀 Como Executar

### 1. Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 2. Instalação
```bash
# Clone ou baixe os arquivos do projeto
# Navegue até a pasta do projeto

# Instale as dependências
pip install -r requirements.txt
```

### 3. Execução
```bash
# Execute o dashboard
python app.py
```

### 4. Acesso
Abra seu navegador e acesse:
```
http://localhost:8050
```

## 📁 Estrutura do Projeto

```
dashboard-algodao/
│
├── app.py                           # Aplicação principal do dashboard
├── dados_algodao.csv               # Dataset com dados de produção
├── brasil_estados_poligonos.geojson # Arquivo GeoJSON dos estados
├── requirements.txt                # Dependências Python
└── README.md                      # Este arquivo
```

## 📊 Dados

### Fonte dos Dados
Os dados utilizados são baseados nas séries históricas do IBGE e CONAB, simulados para demonstração:

- **Período**: 2000-2024
- **Estados**: 19 principais produtores de algodão
- **Regiões**: Norte, Nordeste, Centro-Oeste, Sudeste, Sul
- **Métrica**: Produção em toneladas

### Principais Produtores
1. **Mato Grosso** - Maior produtor nacional
2. **Bahia** - Principal produtor nordestino
3. **Goiás** - Forte produtor do Centro-Oeste
4. **Mato Grosso do Sul** - Crescimento constante
5. **Maranhão** - Destaque no Nordeste

## 🛠️ Tecnologias Utilizadas

- **[Dash](https://dash.plotly.com/)**: Framework web para Python
- **[Plotly](https://plotly.com/python/)**: Biblioteca para visualizações interativas
- **[Pandas](https://pandas.pydata.org/)**: Manipulação e análise de dados
- **[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)**: Componentes UI Bootstrap
- **[GeoJSON](https://geojson.org/)**: Formato para dados geográficos

## 📈 Funcionalidades Avançadas

### Interatividade
- **Filtros Dinâmicos**: Todos os gráficos se atualizam automaticamente
- **Hover Interativo**: Informações detalhadas ao passar o mouse
- **Zoom no Mapa**: Controle de zoom e navegação no mapa
- **Responsividade**: Interface adaptável a mobile e desktop

### Performance
- **Otimização de Dados**: Agregação eficiente para grandes volumes
- **Renderização Rápida**: Templates otimizados do Plotly
- **Filtros Eficientes**: Processamento otimizado dos dados

## 🔧 Customização

### Alterando Dados
Para usar seus próprios dados, substitua o arquivo `dados_algodao.csv` mantendo as colunas:
- `ano`: Ano da produção
- `estado`: Nome do estado
- `sigla`: Sigla do estado (2 letras)
- `regiao`: Região brasileira
- `producao`: Produção em toneladas

### Modificando o GeoJSON
Para usar um mapa mais preciso, substitua o arquivo `brasil_estados_poligonos.geojson` com:
- Coordenadas mais detalhadas dos estados
- IDs correspondentes às siglas dos estados
- Propriedades adicionais se necessário

### Personalizando Temas
No arquivo `app.py`, modifique:
```python
# Alterar temas disponíveis
load_figure_template(["bootstrap", "darkly", "cyborg", "slate"])

# Modificar cores
external_stylesheets=[dbc.themes.BOOTSTRAP]  # Trocar por outro tema
```

## 🐛 Solução de Problemas

### Erro de Importação
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

### Erro no Mapa
- Verificar se o arquivo `brasil_estados_poligonos.geojson` existe
- Conferir se as siglas dos estados coincidem entre CSV e GeoJSON

### Performance Lenta
- Reduzir o range de anos selecionado
- Usar filtros para diminuir o volume de dados
- Considerar agregar dados por período

## 📝 Licença

Este projeto é para fins educacionais e demonstrativos. Dados reais devem ser obtidos de fontes oficiais como IBGE, CONAB e órgãos competentes.

## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou sugestões sobre este dashboard, entre em contato ou abra uma issue no repositório.

---

Desenvolvido com ❤️ usando Python e Plotly Dash
