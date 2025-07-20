
# Teste rápido do dashboard
# Execute este arquivo para verificar se as dependências estão corretas

import sys

print("🧪 Testando dependências do Dashboard de Algodão...")
print("="*50)

# Lista de dependências para testar
dependencias = [
    'dash', 'plotly', 'pandas', 'json', 
    'dash_bootstrap_components', 'dash_bootstrap_templates'
]

erros = []

for dep in dependencias:
    try:
        if dep == 'dash_bootstrap_components':
            import dash_bootstrap_components as dbc
            print(f"✅ {dep} - OK")
        elif dep == 'dash_bootstrap_templates':
            from dash_bootstrap_templates import load_figure_template
            print(f"✅ {dep} - OK")
        elif dep == 'json':
            import json
            print(f"✅ {dep} - OK")
        else:
            __import__(dep)
            print(f"✅ {dep} - OK")
    except ImportError:
        print(f"❌ {dep} - ERRO: Não instalado")
        erros.append(dep)

print("="*50)

if erros:
    print(f"❌ {len(erros)} erro(s) encontrado(s):")
    for erro in erros:
        print(f"   - {erro}")
    print("\n📦 Para corrigir, execute:")
    print("   pip install -r requirements.txt")
else:
    print("✅ Todas as dependências OK!")
    print("\n🚀 Você pode executar o dashboard com:")
    print("   python app.py")

# Verificar arquivos necessários
print("\n📁 Verificando arquivos necessários...")

arquivos = ['dados_algodao.csv', 'brasil_estados_poligonos.geojson']
for arquivo in arquivos:
    try:
        with open(arquivo, 'r') as f:
            print(f"✅ {arquivo} - OK")
    except FileNotFoundError:
        print(f"❌ {arquivo} - ERRO: Arquivo não encontrado")

print("\n🎯 Teste concluído!")
