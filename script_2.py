# Criar o arquivo app.py com o dashboard completo
app_code = '''
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# ============================================================================
# CONFIGURAÇÃO INICIAL
# ============================================================================

# Carregar templates de figura
load_figure_template(["bootstrap", "darkly"])

# Inicializar app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ============================================================================
# CARREGAMENTO DE DADOS
# ============================================================================

# Carregar dados de produção
df = pd.read_csv('dados_algodao.csv')

# Carregar GeoJSON dos estados
with open('brasil_estados_poligonos.geojson', 'r') as f:
    geojson_brasil = json.load(f)

# Preparar listas para filtros
anos = sorted(df['ano'].unique())
regioes = sorted(df['regiao'].unique())
estados = sorted(df['estado'].unique())

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def formatar_numero(num):
    """Formata números para exibição amigável"""
    if num >= 1000000:
        return f'{num/1000000:.1f}M'
    elif num >= 1000:
        return f'{num/1000:.0f}K'
    else:
        return str(num)

def calcular_metricas(df_filtrado):
    """Calcula métricas principais do dashboard"""
    if df_filtrado.empty:
        return {
            'producao_total': 0,
            'media_anual': 0,
            'estado_lider': 'N/A',
            'crescimento': 0
        }
    
    producao_total = df_filtrado['producao'].sum()
    media_anual = df_filtrado.groupby('ano')['producao'].sum().mean()
    
    # Estado líder
    estado_lider = df_filtrado.groupby('estado')['producao'].sum().idxmax()
    
    # Crescimento (primeiro vs último ano disponível)
    anos_disp = sorted(df_filtrado['ano'].unique())
    if len(anos_disp) >= 2:
        prod_inicial = df_filtrado[df_filtrado['ano'] == anos_disp[0]]['producao'].sum()
        prod_final = df_filtrado[df_filtrado['ano'] == anos_disp[-1]]['producao'].sum()
        crescimento = ((prod_final - prod_inicial) / prod_inicial * 100) if prod_inicial > 0 else 0
    else:
        crescimento = 0
    
    return {
        'producao_total': producao_total,
        'media_anual': media_anual,
        'estado_lider': estado_lider,
        'crescimento': crescimento
    }

# ============================================================================
# LAYOUT DO DASHBOARD
# ============================================================================

app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("🌱 Dashboard Produção de Algodão - Brasil", 
                       className="text-center mb-0"),
                html.P("Análise da série histórica de produção por estados e regiões",
                       className="text-center text-muted mb-3"),
                dbc.Button("🌙 Dark Mode", id="dark-mode-toggle", color="secondary", 
                          size="sm", className="position-absolute", style={"top": "10px", "right": "10px"})
            ], style={"position": "relative"})
        ])
    ], className="mb-4"),
    
    # Filtros
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🎛️ Filtros", className="card-title"),
                    
                    # Range de Anos
                    html.Label("📅 Período:", className="fw-bold"),
                    dcc.RangeSlider(
                        id='range-slider-ano',
                        min=min(anos),
                        max=max(anos),
                        value=[min(anos), max(anos)],
                        marks={ano: str(ano) for ano in range(min(anos), max(anos)+1, 5)},
                        step=1,
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                    
                    # Filtros em linha
                    dbc.Row([
                        dbc.Col([
                            html.Label("🗺️ Regiões:", className="fw-bold"),
                            dcc.Dropdown(
                                id='dropdown-regiao',
                                options=[{'label': regiao, 'value': regiao} for regiao in regioes],
                                multi=True,
                                placeholder="Todas as regiões"
                            )
                        ], md=4),
                        dbc.Col([
                            html.Label("📍 Estados:", className="fw-bold"),
                            dcc.Dropdown(
                                id='dropdown-estado',
                                options=[{'label': estado, 'value': estado} for estado in estados],
                                multi=True,
                                placeholder="Todos os estados"
                            )
                        ], md=4),
                        dbc.Col([
                            html.Label("📊 Ordenar por:", className="fw-bold"),
                            dcc.Dropdown(
                                id='dropdown-ordenacao',
                                options=[
                                    {'label': 'Produção Total', 'value': 'producao'},
                                    {'label': 'Nome do Estado', 'value': 'estado'},
                                    {'label': 'Região', 'value': 'regiao'}
                                ],
                                value='producao',
                                clearable=False
                            )
                        ], md=4)
                    ])
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Cards de Métricas
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="metrica-total", className="text-primary"),
                    html.P("📈 Produção Total", className="text-muted mb-0")
                ])
            ], className="h-100")
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="metrica-media", className="text-info"),
                    html.P("📊 Média Anual", className="text-muted mb-0")
                ])
            ], className="h-100")
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="metrica-lider", className="text-success"),
                    html.P("🏆 Estado Líder", className="text-muted mb-0")
                ])
            ], className="h-100")
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="metrica-crescimento", className="text-warning"),
                    html.P("📈 Crescimento", className="text-muted mb-0")
                ])
            ], className="h-100")
        ], md=3)
    ], className="mb-4"),
    
    # Visualizações Principais
    dbc.Row([
        # Mapa do Brasil
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("🗺️ Mapa de Calor - Estados do Brasil", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id='mapa-brasil')
                ])
            ])
        ], lg=6),
        
        # Gráfico de Série Temporal
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("📈 Evolução Temporal da Produção", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id='serie-temporal')
                ])
            ])
        ], lg=6)
    ], className="mb-4"),
    
    # Visualizações Secundárias
    dbc.Row([
        # Top Estados
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("🏆 Top 10 Estados Produtores", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id='top-estados')
                ])
            ])
        ], lg=6),
        
        # Distribuição por Região
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("🍰 Distribuição por Região", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id='distribuicao-regiao')
                ])
            ])
        ], lg=6)
    ], className="mb-4"),
    
    # Tabela de Dados
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("📋 Dados Detalhados", className="mb-0")),
                dbc.CardBody([
                    html.Div(id='tabela-dados')
                ])
            ])
        ])
    ]),
    
    # Store para tema
    dcc.Store(id='theme-store', data={'theme': 'bootstrap'})
    
], fluid=True, className="py-3")

# ============================================================================
# CALLBACKS
# ============================================================================

# Callback para toggle do dark mode
@callback(
    Output('theme-store', 'data'),
    Input('dark-mode-toggle', 'n_clicks'),
    prevent_initial_call=True
)
def toggle_theme(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return {'theme': 'darkly'}
    return {'theme': 'bootstrap'}

# Callback principal para atualizar todas as visualizações
@callback(
    [Output('mapa-brasil', 'figure'),
     Output('serie-temporal', 'figure'),
     Output('top-estados', 'figure'),
     Output('distribuicao-regiao', 'figure'),
     Output('tabela-dados', 'children'),
     Output('metrica-total', 'children'),
     Output('metrica-media', 'children'),
     Output('metrica-lider', 'children'),
     Output('metrica-crescimento', 'children')],
    [Input('range-slider-ano', 'value'),
     Input('dropdown-regiao', 'value'),
     Input('dropdown-estado', 'value'),
     Input('dropdown-ordenacao', 'value'),
     Input('theme-store', 'data')]
)
def update_dashboard(range_ano, regioes_selecionadas, estados_selecionados, 
                    ordenacao, theme_data):
    
    # Filtrar dados
    df_filtrado = df[
        (df['ano'] >= range_ano[0]) & 
        (df['ano'] <= range_ano[1])
    ]
    
    if regioes_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['regiao'].isin(regioes_selecionadas)]
    
    if estados_selecionados:
        df_filtrado = df_filtrado[df_filtrado['estado'].isin(estados_selecionados)]
    
    # Tema
    template = theme_data['theme']
    
    # ========================================================================
    # 1. MAPA DE CALOR DO BRASIL
    # ========================================================================
    
    # Agregar dados por estado para o mapa
    df_mapa = df_filtrado.groupby(['sigla', 'estado', 'regiao'])['producao'].sum().reset_index()
    
    fig_mapa = px.choropleth_mapbox(
        df_mapa,
        geojson=geojson_brasil,
        locations='sigla',
        color='producao',
        hover_name='estado',
        hover_data={'regiao': True, 'producao': ':,'},
        color_continuous_scale='Viridis',
        mapbox_style="carto-positron",
        zoom=3.5,
        center={"lat": -14, "lon": -55},
        opacity=0.7,
        labels={'producao': 'Produção (ton)'},
        template=template
    )
    
    fig_mapa.update_layout(
        title="Produção de Algodão por Estado",
        margin={"r":0,"t":30,"l":0,"b":0},
        coloraxis_colorbar=dict(title="Produção (ton)")
    )
    
    # ========================================================================
    # 2. SÉRIE TEMPORAL
    # ========================================================================
    
    df_temporal = df_filtrado.groupby('ano')['producao'].sum().reset_index()
    
    fig_temporal = px.line(
        df_temporal, 
        x='ano', 
        y='producao',
        title='Evolução da Produção Nacional',
        template=template
    )
    
    fig_temporal.update_traces(line=dict(width=3))
    fig_temporal.update_layout(
        xaxis_title="Ano",
        yaxis_title="Produção (toneladas)",
        hovermode='x unified'
    )
    
    # ========================================================================
    # 3. TOP ESTADOS
    # ========================================================================
    
    df_top = df_filtrado.groupby(['estado', 'regiao'])['producao'].sum().reset_index()
    df_top = df_top.sort_values('producao', ascending=True).tail(10)
    
    fig_top = px.bar(
        df_top,
        x='producao',
        y='estado',
        color='regiao',
        orientation='h',
        title='Top 10 Estados Produtores',
        template=template
    )
    
    fig_top.update_layout(
        xaxis_title="Produção (toneladas)",
        yaxis_title="Estado",
        legend_title="Região"
    )
    
    # ========================================================================
    # 4. DISTRIBUIÇÃO POR REGIÃO
    # ========================================================================
    
    df_regiao = df_filtrado.groupby('regiao')['producao'].sum().reset_index()
    
    fig_regiao = px.pie(
        df_regiao,
        values='producao',
        names='regiao',
        title='Distribuição da Produção por Região',
        template=template
    )
    
    # ========================================================================
    # 5. TABELA DE DADOS
    # ========================================================================
    
    df_tabela = df_filtrado.groupby(['estado', 'regiao', 'ano'])['producao'].sum().reset_index()
    df_tabela['producao_formatada'] = df_tabela['producao'].apply(lambda x: f"{x:,}")
    
    if ordenacao == 'producao':
        df_tabela = df_tabela.sort_values('producao', ascending=False)
    else:
        df_tabela = df_tabela.sort_values(ordenacao)
    
    # Limitar a 100 registros para performance
    df_tabela_show = df_tabela.head(100)
    
    tabela = dbc.Table.from_dataframe(
        df_tabela_show[['estado', 'regiao', 'ano', 'producao_formatada']].rename(columns={
            'estado': 'Estado',
            'regiao': 'Região', 
            'ano': 'Ano',
            'producao_formatada': 'Produção (ton)'
        }),
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        size='sm'
    )
    
    # ========================================================================
    # 6. MÉTRICAS
    # ========================================================================
    
    metricas = calcular_metricas(df_filtrado)
    
    return (
        fig_mapa,
        fig_temporal, 
        fig_top,
        fig_regiao,
        tabela,
        formatar_numero(metricas['producao_total']) + " ton",
        formatar_numero(metricas['media_anual']) + " ton/ano",
        metricas['estado_lider'],
        f"{metricas['crescimento']:.1f}%"
    )

# ============================================================================
# EXECUTAR APP
# ============================================================================

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
'''

# Salvar o código do app
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

print("✅ Arquivo app.py criado com sucesso!")
print("\nPara executar o dashboard:")
print("1. Instale as dependências:")
print("   pip install dash plotly pandas dash-bootstrap-components dash-bootstrap-templates")
print("\n2. Execute o dashboard:")
print("   python app.py")
print("\n3. Abra no navegador:")
print("   http://localhost:8050")

print("\n📁 Arquivos criados:")
print("   - app.py (aplicação principal)")
print("   - dados_algodao.csv (dados de produção)")
print("   - brasil_estados_poligonos.geojson (mapa dos estados)")

print(f"\n📊 Funcionalidades implementadas:")
print("   ✅ Mapa de calor interativo do Brasil")
print("   ✅ Filtros dinâmicos (ano, região, estado)")
print("   ✅ Gráfico de série temporal")
print("   ✅ Top 10 estados produtores")
print("   ✅ Distribuição por região (pizza)")
print("   ✅ Tabela de dados detalhados")
print("   ✅ Cards com métricas principais")
print("   ✅ Toggle para modo escuro/claro")
print("   ✅ Design responsivo e moderno")