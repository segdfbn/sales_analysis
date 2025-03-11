from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np
import pandas as pd

# Sample sales data
np.random.seed(42)  # For reproducibility
data = {
    'Date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'Region': np.random.choice(['North America', 'Europe', 'Asia', 'South America'], size=100),
    'Country': np.random.choice(['USA', 'Germany', 'Japan', 'Brazil'], size=100),
    'Product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], size=100),
    'Price': np.random.randint(10, 50, size=100),
    'Quantity_Sold': np.random.randint(50, 300, size=100)
}

# Create DataFrame
df = pd.DataFrame(data)
# Calculate sales
df['Sales'] = df['Price'] * df['Quantity_Sold']

df.to_csv('sales_data.csv',index=False)
app = Dash(__name__)


app.layout = html.Div([
    html.H4('Interactive scatter plot with Iris dataset'),
    dcc.Graph(id="scatter-plot"),
    html.P("Filter by petal width:"),
    dcc.RangeSlider(
        id='range-slider',
        min=df['Price'].min(), max=df['Price'].max(), step=(df['Price'].max())/10,
        marks={0: '0', 50: '50'},
        # marks={for x in df['Price'].max()0: '0', 50: '50'},
        value=[0, 50]
    ),
])


@app.callback(
    Output("scatter-plot", "figure"), 
    Input("range-slider", "value"))
def update_bar_chart(slider_range):
    # df = px.data.iris() # replace with your own data source
    low, high = slider_range
    mask = (df['Price'] > low) & (df['Price'] < high)
    fig = px.scatter(
        df[mask], x='Price', y='Sales',
        size='Quantity_Sold',color='Country', 
        hover_data=['Product'])
    return fig


app.run_server(debug=True)