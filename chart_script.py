import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the cotton production data
df = pd.read_csv("dados_algodao.csv")

# Aggregate data by year and region
df_agg = df.groupby(['ano', 'regiao'])['producao'].sum().reset_index()

# Create the time series chart
fig = px.line(df_agg, 
              x='ano', 
              y='producao', 
              color='regiao',
              color_discrete_sequence=['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F', '#D2BA4C'])

# Update layout with title and formatting
fig.update_layout(
    title="Evolução Produção Algodão por Região",
    xaxis_title="Ano",
    yaxis_title="Produção (t)",
    legend=dict(
        orientation='h', 
        yanchor='bottom', 
        y=1.05, 
        xanchor='center', 
        x=0.5,
        title="Região"
    )
)

# Format y-axis to show values in millions/billions with abbreviations
fig.update_yaxes(
    tickformat='.2s'
)

# Update traces to set cliponaxis=False (this is the correct place for this property)
fig.update_traces(cliponaxis=False)

# Update hover template to show abbreviated values
fig.update_traces(
    hovertemplate="<b>%{fullData.name}</b><br>" +
                  "Ano: %{x}<br>" +
                  "Produção: %{y:,.0f}t<br>" +
                  "<extra></extra>"
)

# Save the chart
fig.write_image("cotton_production_regions.png")

# Display summary statistics
print("Data summary by region:")
print(df_agg.groupby('regiao')['producao'].agg(['mean', 'max', 'min']))