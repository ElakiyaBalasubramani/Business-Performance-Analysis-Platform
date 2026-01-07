
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# Generate date range
dates = [datetime(2025, 1, 1) + timedelta(days=x) for x in range(30)]

# Generate mock data
data = {
    'Date': dates,
    'Revenue': np.random.randint(4000, 8000, size=30),
    'Expenses': np.random.randint(3000, 5000, size=30),
    'Sales_Volume': np.random.randint(80, 150, size=30),
    'Customer_Satisfaction': np.round(np.random.uniform(3.5, 5.0, size=30), 1)
}

df = pd.DataFrame(data)

# Calculate Profit
df['Profit'] = df['Revenue'] - df['Expenses']

# Save to CSV
csv_path = 'sample_business_data.csv'
df.to_csv(csv_path, index=False)
print(f"Created {csv_path}")

# Save to Excel
xlsx_path = 'sample_business_data.xlsx'
df.to_excel(xlsx_path, index=False)
print(f"Created {xlsx_path}")
