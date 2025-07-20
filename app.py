
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
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
from dash_bootstrap_templates import load_figure_template, ThemeSwitchAIO

app = dash.Dash(__name__)#, external_stylesheets=[dbc.themes.DARKLY])
#app = dash.Dash(__name__)

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

#html.Link(rel="stylesheet", href=dbc.themes.BOOTSTRAP, id="theme-link")


@callback(
    Output('theme-link', 'href'),
    Input('theme-store', 'data')
)
def alternar_tema_css(theme_data):
    if theme_data is None:
        return dbc.themes.BOOTSTRAP  # fallback padrão
    tema = theme_data.get('theme', 'bootstrap')
    if tema == 'darkly':
        return dbc.themes.DARKLY
    return dbc.themes.BOOTSTRAP

# ============================================================================
# LAYOUT DO DASHBOARD
# ============================================================================

app.layout = html.Div([
    # Inclusão dinâmica do tema via href
    html.Link(rel="stylesheet", href=dbc.themes.BOOTSTRAP, id="theme-link"),
    

    dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("🌱 Dashboard Produção de Algodão - Brasil", 
                           className="text-center mb-0"),
                    html.P("Análise da série histórica de produção por estados e regiões",
                           className="text-center text-muted mb-3"),
                    dbc.Button(id="dark-mode-toggle", color="secondary", size="sm",
                        className="position-absolute", style={"top": "10px", "right": "10px"})
                ], style={"position": "relative"})
            ])
        ], className="mb-4"),

        # Filtros
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("🎛️ Filtros", className="card-title"),
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

        # Gráficos principais
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🗺️ Mapa de Calor - Estados do Brasil", className="mb-0")),
                    dbc.CardBody([dcc.Graph(id='mapa-brasil')])
                ])
            ], lg=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📈 Evolução Temporal da Produção", className="mb-0")),
                    dbc.CardBody([dcc.Graph(id='serie-temporal')])
                ])
            ], lg=6)
        ], className="mb-4"),

        # Gráficos secundários
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🏆 Top 10 Estados Produtores", className="mb-0")),
                    dbc.CardBody([dcc.Graph(id='top-estados')])
                ])
            ], lg=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🍰 Distribuição por Região", className="mb-0")),
                    dbc.CardBody([dcc.Graph(id='distribuicao-regiao')])
                ])
            ], lg=6)
        ], className="mb-4"),

        # Tabela
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📋 Dados Detalhados", className="mb-0")),
                    dbc.CardBody([html.Div(id='tabela-dados')])
                ])
            ])
        ]),

        # Armazenamento do tema
        dcc.Store(id='theme-store', data={'theme': 'darkly'})
    ], fluid=True, className="py-3")
])


# ============================================================================
# CALLBACKS
# ============================================================================

# Callback para toggle do dark mode
@callback(
    Output('theme-store', 'data'),
    Input('dark-mode-toggle', 'n_clicks'),
    prevent_initial_call=True,
    allow_duplicate=True
)
def toggle_theme(n_clicks):
    # Esta função não precisa fazer nada. A lógica real está abaixo.
    pass
from dash import State

@callback(
    Output('theme-store', 'data', allow_duplicate=True),
    Input('dark-mode-toggle', 'n_clicks'),
    State('theme-store', 'data'),
    prevent_initial_call=True
)
def toggle_theme_click(n_clicks, theme_data):
    current = theme_data.get('theme', 'darkly')
    new_theme = 'bootstrap' if current == 'darkly' else 'darkly'
    return {'theme': new_theme}


@callback(
    Output('dark-mode-toggle', 'children'),
    Input('theme-store', 'data')
)
def atualizar_botao_tema(theme_data):
    if theme_data is None:
        return "🌙 Dark Mode"  # fallback
    return "☀️ Light Mode" if theme_data.get('theme', 'bootstrap') == 'darkly' else "🌙 Dark Mode"


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
    if theme_data is None:
        theme_data = {'theme': 'bootstrap'}

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

    # fig_mapa = px.choropleth_mapbox(
    #     df_mapa,
    #     geojson=geojson_brasil,
    #     locations='sigla',
    #     color='producao',
    #     hover_name='estado',
    #     hover_data={'regiao': True, 'producao': ':,'},
    #     color_continuous_scale='Viridis',
    #     mapbox_style="carto-positron",
    #     zoom=3.5,
    #     center={"lat": -14, "lon": -55},
    #     opacity=0.7,
    #     labels={'producao': 'Produção (ton)'},
    #     template=template
    # )
    # Obter coordenadas centrais dos estados (você pode carregar isso de um CSV auxiliar ou definir manualmente)
    coordenadas_estados = {
        'MT': [-56.1, -12.7],
        'BA': [-41.7, -12.9],
        'GO': [-49.6, -15.9],
        'MS': [-54.5, -20.5],
        'MA': [-45.2, -5.4],
        'PI': [-42.3, -7.5],
        'CE': [-39.5, -5.2],
        'MG': [-44.4, -18.1],
        'SP': [-48.6, -22.5],
        'PR': [-51.5, -24.9],
        'TO': [-48.2, -10.3],
        'PA': [-52.0, -3.8],
        'AL': [-36.6, -9.6],
        'PB': [-36.7, -7.0],
        'RN': [-36.7, -5.8],
        'PE': [-37.8, -8.3],
        'SE': [-37.4, -10.6],
        'RO': [-63.9, -10.8],
        'DF': [-47.9, -15.8]
    }

    # Adiciona colunas de latitude e longitude
    df_mapa['lat'] = df_mapa['sigla'].map(lambda x: coordenadas_estados[x][1])
    df_mapa['lon'] = df_mapa['sigla'].map(lambda x: coordenadas_estados[x][0])

    mapbox_style = "carto-darkmatter" if template == "darkly" else "carto-positron"
    # Criar bolhas proporcionais
    fig_mapa = px.scatter_mapbox(
        df_mapa,
        lat='lat',
        lon='lon',
        size='producao',
        color='regiao',
        hover_name='estado',
        hover_data={'producao': ':,'},
        size_max=50,
        zoom=3.5,
        # Definir estilo do mapa com base no tema
        mapbox_style = mapbox_style,#"carto-darkmatter",

        center={"lat": -14, "lon": -55},
        template=template
    )

    # fig_mapa.update_layout(
    #     title="Produção de Algodão por Estado (Mapa de Bolhas)",
    #     margin={"r":0,"t":30,"l":0,"b":0}
    # )


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
    app.run(debug=True, host='0.0.0.0', port=8050)

