import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output,no_update
import dash_bootstrap_components as dbc
import os


df = pd.read_csv(os.path.join(os.path.dirname(__file__),'../data/sales_data.csv'))
df['Sales'] = df['Price'] * df['Quantity_Sold']
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.to_period('M')


SHADOW_STYLE = {'margin-bottom':'10px','border':'1px', 'boxShadow':'0 4px 8px rgba(0,0,0,0.1)'}
# Initialize Dash app
app = Dash(__name__,external_stylesheets=[dbc.themes.LUX])
# App layout
app.layout = html.Div(
    style={'padding':'10px'},
    children=[
    dbc.Row(
        dbc.CardBody(html.H1("Global Sales Dashboard", style={'textAlign': 'center'}))
    ),
    dbc.Row([
        dbc.Col(width=3, children=[
            html.Label("Select Region:"),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region, 'value': region} for region in df['Region'].unique()],
                value='North America',
                clearable=False
            ),
        ]),
        dbc.Col(width=9, children=[
            dcc.Graph(id='sales-by-region',style=SHADOW_STYLE),
            dcc.Graph(id='monthly-sales-trend',style= SHADOW_STYLE),
            dcc.Graph(id='top-products',style= SHADOW_STYLE),
            dcc.Graph(id='correlation-heatmap',style= SHADOW_STYLE)
        ])
    ]),
])

# Callbacks to update graphs
@app.callback(
    [Output('sales-by-region', 'figure'),
     Output('monthly-sales-trend', 'figure'),
     Output('top-products', 'figure'),
     Output('correlation-heatmap', 'figure')],
    [Input('region-dropdown', 'value')]
)
def update_graphs(selected_region):
    filtered_df = df[df['Region'] == selected_region]
    # Sales by region
    sales_by_region = px.scatter(df,
                                 x='Price', y='Sales',
                                 size='Quantity_Sold',color='Country',
                                 title='Sales by Country')

    # Monthly sales trend
    filtered_df['Month'] = filtered_df['Date'].dt.to_period('M').astype('string')
    monthly_sales = px.scatter(filtered_df.groupby(['Month'])['Sales'].sum().reset_index(),
                            x='Month', y='Sales',
                            color="Month", size='Sales',
                            hover_data=['Sales'],
                            title='Monthly Sales Trend')

    # Top 10 products
    top_products = px.bar(filtered_df.groupby('Product')['Sales'].sum().reset_index().nlargest(10, 'Sales'),
                           x='Product', y='Sales',
                           title='Top 10 Products by Sales')

    # Correlation heatmap
    corr = filtered_df[['Price', 'Quantity_Sold', 'Sales']].corr()
    heatmap = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.index,
        colorscale='Viridis'))
    heatmap.update_layout(title='Correlation Heatmap')
    return [sales_by_region, monthly_sales, top_products, heatmap]
    # return [sales_by_region, no_update, top_products, heatmap ]

# Run app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True)