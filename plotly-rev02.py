import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go

# Leitura dos DATAFRAMES
df_2016 = pd.read_excel('data-2016.xlsx')
df_2020 = pd.read_excel('data-2022.xlsx')

# Alterações necessárias...
# 2. Alterar "NM_VOTAVEL" por "CANDIDATO"
df_2016.rename(columns={'NM_VOTAVEL': 'CANDIDATO'}, inplace=True)
df_2020.rename(columns={'NM_VOTAVEL': 'CANDIDATO'}, inplace=True)

# Identificar as 5 NR_SECAO mais votadas em 2016
top_secoes_2016 = df_2016.groupby('NR_SECAO')['QT_VOTOS'].sum().nlargest(5).index
dados_top_secoes_2016 = df_2016[df_2016['NR_SECAO'].isin(top_secoes_2016)]

# Identificar as 5 NR_SECAO menos votadas em 2016
bottom_secoes_2016 = df_2016.groupby('NR_SECAO')['QT_VOTOS'].sum().nsmallest(5).index
dados_bottom_secoes_2016 = df_2016[df_2016['NR_SECAO'].isin(bottom_secoes_2016)]

# Identificar as 5 NR_SECAO mais votadas em 2020
top_secoes_2020 = df_2020.groupby('NR_SECAO')['QT_VOTOS'].sum().nlargest(5).index
dados_top_secoes_2020 = df_2020[df_2020['NR_SECAO'].isin(top_secoes_2020)]

# Identificar as 5 NR_SECAO menos votadas em 2020
bottom_secoes_2020 = df_2020.groupby('NR_SECAO')['QT_VOTOS'].sum().nsmallest(5).index
dados_bottom_secoes_2020 = df_2020[df_2020['NR_SECAO'].isin(bottom_secoes_2020)]

# Criar DataFrames com as informações
df_top_secoes_2016 = dados_top_secoes_2016.groupby('NR_SECAO')['QT_VOTOS'].sum().reset_index()
df_top_secoes_2016.columns = ['NR_SECAO', 'QT_VOTOS_2016']

df_bottom_secoes_2016 = dados_bottom_secoes_2016.groupby('NR_SECAO')['QT_VOTOS'].sum().reset_index()
df_bottom_secoes_2016.columns = ['NR_SECAO', 'QT_VOTOS_BOTTOM_2016']

df_top_secoes_2020 = dados_top_secoes_2020.groupby('NR_SECAO')['QT_VOTOS'].sum().reset_index()
df_top_secoes_2020.columns = ['NR_SECAO', 'QT_VOTOS_2020']

df_bottom_secoes_2020 = dados_bottom_secoes_2020.groupby('NR_SECAO')['QT_VOTOS'].sum().reset_index()
df_bottom_secoes_2020.columns = ['NR_SECAO', 'QT_VOTOS_BOTTOM_2020']

# Calcular total de votos em 2016 e 2020
total_votos_2016 = df_2016['QT_VOTOS'].sum()
total_votos_2020 = df_2020['QT_VOTOS'].sum()

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div(children=[
    html.H1(children='ANÁLISE ELEIÇÕES 2016 - 2020',  style={'textAlign': 'center', 'color': '#120a8f'}),

    # Parte superior para gráficos de 2020
    html.Div(children=[
        # Gráfico de pizza para os mais votados em 2020 (lado esquerdo)
        dcc.Graph(
            id='top-secoes-2020',
            figure=go.Figure(data=[go.Pie(labels=df_top_secoes_2020['NR_SECAO'],
                                           values=df_top_secoes_2020['QT_VOTOS_2020'],
                                           hoverinfo="label+percent+value",
                                           textinfo='label+value+percent')]).update_layout(title='5 SEÇÕES MAIS VOTOS EM 2020 - CLEVINHO',
                                                                                              legend=dict(x=0, y=1))
        ),

        # Gráfico de pizza para os menos votados em 2020 (lado direito)
        dcc.Graph(
            id='bottom-secoes-2020',
            figure=go.Figure(data=[go.Pie(labels=df_bottom_secoes_2020['NR_SECAO'],
                                           values=df_bottom_secoes_2020['QT_VOTOS_BOTTOM_2020'],
                                           hoverinfo="label+percent+value",
                                           textinfo='label+value+percent')]).update_layout(title='5 SEÇÕES MENOS VOTOS EM 2020 - CLEVINHO',
                                                                                              legend=dict(x=0, y=1))
        ),
    ], style={'display': 'flex'}),

    # Parte inferior para gráficos de 2016
    html.Div(children=[
        # Gráfico de pizza para os mais votados em 2016 (lado esquerdo)
        dcc.Graph(
            id='top-secoes-2016',
            figure=go.Figure(data=[go.Pie(labels=df_top_secoes_2016['NR_SECAO'],
                                           values=df_top_secoes_2016['QT_VOTOS_2016'],
                                           hoverinfo="label+percent+value",
                                           textinfo='label+value+percent')]).update_layout(title='5 SEÇÕES MAIS VOTOS EM 2016 - CLEVINHO',
                                                                                              legend=dict(x=0, y=1))
        ),

        # Gráfico de pizza para os menos votados em 2016 (lado direito)
        dcc.Graph(
            id='bottom-secoes-2016',
            figure=go.Figure(data=[go.Pie(labels=df_bottom_secoes_2016['NR_SECAO'],
                                           values=df_bottom_secoes_2016['QT_VOTOS_BOTTOM_2016'],
                                           hoverinfo="label+percent+value",
                                           textinfo='label+value+percent')]).update_layout(title='5 SEÇÕES MENOS VOTOS EM 2020 - CLEVINHO',
                                                                                              legend=dict(x=0, y=1))
        ),
    ], style={'display': 'flex'}),

    # Gráfico de barra para total de votos
    dcc.Graph(
        id='total-votos-bar',
        figure=go.Figure(data=[go.Bar(x=['2016', '2020'],
                                      y=[total_votos_2016, total_votos_2020],
                                      text=[f'TOTAL - {total_votos_2016}', f'TOTAL -  {total_votos_2020}'],
                                      hoverinfo='text')]).update_layout(title='VOTOS TOTAIS 2016 - 2020',
                                                                           xaxis_title='ANOS',
                                                                          yaxis_title='VOTOS',
                                                                           legend=dict(x=0, y=1),
                                                                           title_x=0.5, # Centraliza o título horizontalmente
            ),
    ),

    # Texto com o total de votos no meio da tela
    html.H2(children=f"TOTAL VOTOS - 2016 = {total_votos_2016} / TOTAL VOTOS - 2020 = {total_votos_2020}",
            style={'textAlign': 'center', 'color': '#120a8f'}),
    # ... Adicione outros gráficos e componentes conforme necessário ...

], style={'width': '100%', 'margin': 'auto', 'backgroundColor': '#f0f0f0'})

# Executar o aplicativo
if __name__ == '__main__':
    print("Relatório Clevinho está rodando em http://127.0.0.1:8080/")
    app.run_server(debug=True, host='127.0.0.1', port=8080)
