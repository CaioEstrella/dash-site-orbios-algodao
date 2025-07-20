
# Configurações para produção
# Modifique estas configurações conforme necessário

# Configurações do servidor
HOST = '0.0.0.0'  # Para aceitar conexões externas use '0.0.0.0', para local use '127.0.0.1'
PORT = 8050       # Porta do servidor
DEBUG = False     # Mudar para False em produção

# Configurações de dados
MAX_RECORDS_TABLE = 100  # Máximo de registros na tabela
CACHE_TIMEOUT = 300      # Timeout do cache em segundos

# Temas disponíveis
THEMES = {
    'light': 'bootstrap',
    'dark': 'darkly',
    'alternative': 'cyborg'
}

# Configurações do mapa
MAP_CENTER = {"lat": -14, "lon": -55}  # Centro do mapa (Brasil)
MAP_ZOOM = 3.5                         # Zoom inicial
MAP_STYLE = "carto-positron"           # Estilo do mapa

# Configurações de performance
ENABLE_CACHING = True
MAX_FILTER_COMBINATIONS = 1000
