import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output,no_update


# Sample sales data
data = {
    'Date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'Region': ['North America', 'Europe', 'Asia', 'South America'] * 25,
    'Country': ['USA', 'Germany', 'Japan', 'Brazil'] * 25,
    'Product': ['Product A', 'Product B', 'Product C', 'Product D'] * 25,
    'Price': [10, 20, 30, 40] * 25,
    'Quantity_Sold': [100, 150, 200, 250] * 25
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate sales
df['Sales'] = df['Price'] * df['Quantity_Sold']

# Initialize Dash app
app = Dash(__name__)
# App layout
app.layout = html.Div([
    html.H1("Global Sales Dashboard", style={'textAlign': 'center'}),

    html.Label("Select Region:"),
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': region, 'value': region} for region in df['Region'].unique()],
        value='North America',
        clearable=False
    ),

    dcc.Graph(id='sales-by-region'),
    dcc.Graph(id='monthly-sales-trend'),
    dcc.Graph(id='top-products'),
    dcc.Graph(id='correlation-heatmap')
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
    sales_by_region = px.bar(filtered_df.groupby('Country')['Sales'].sum().reset_index(),
                             x='Country', y='Sales',
                             title='Sales by Country')

    # Monthly sales trend
    print("==========================================")
    print(filtered_df.groupby('Country')['Sales'].sum().reset_index())
    filtered_df['Month'] = filtered_df['Date'].dt.to_period('M').astype('string')
    print(filtered_df.groupby('Month')['Sales'].sum().reset_index())
    monthly_sales = px.line(filtered_df.groupby('Month')['Sales'].sum().reset_index(),
                            x='Month', y='Sales',
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
    # return [sales_by_region, monthly_sales, top_products, heatmap ]

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)