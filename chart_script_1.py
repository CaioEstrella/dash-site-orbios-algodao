import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load the cotton data
df = pd.read_csv("dados_algodao.csv")

# Filter data for 2020-2024
df_filtered = df[df['ano'].between(2020, 2024)]

# Aggregate production by state and region for 2020-2024
state_production = df_filtered.groupby(['estado', 'regiao'])['producao'].sum().reset_index()

# Sort by production and get top 10
top_10 = state_production.sort_values('producao', ascending=False).head(10)

# Define region colors using the brand colors
region_colors = {
    'Centro-Oeste': '#1FB8CD',  # Strong cyan
    'Nordeste': '#FFC185',      # Light orange  
    'Sudeste': '#ECEBD5',       # Light green
    'Norte': '#5D878F',         # Cyan
    'Sul': '#D2BA4C'            # Moderate yellow
}

# Create horizontal bar chart
fig = go.Figure()

for region in top_10['regiao'].unique():
    region_data = top_10[top_10['regiao'] == region]
    
    fig.add_trace(go.Bar(
        x=region_data['producao'],
        y=region_data['estado'],
        orientation='h',
        name=region,
        marker_color=region_colors[region],
        text=[f'{val/1000000:.1f}m' for val in region_data['producao']],
        textposition='inside',
        cliponaxis=False
    ))

# Update layout
fig.update_layout(
    title="Top 10 Estados Produtores de Algodão (2020-2024)",
    xaxis_title="Produção (t)",
    yaxis_title="Estados",
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    yaxis=dict(categoryorder='total ascending')
)

# Update x-axis to show abbreviated values
fig.update_xaxes(
    tickformat='.1s'
)

# Save the chart
fig.write_image("cotton_chart.png")
print("Chart saved successfully!")