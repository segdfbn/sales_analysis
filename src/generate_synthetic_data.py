import pandas as pd
import os
import numpy as np

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
df.to_csv(os.path.join(os.path.dirname(__file__),'../data/sales_data.csv'),index=False)