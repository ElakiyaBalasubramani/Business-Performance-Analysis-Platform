
import pandas as pd
import numpy as np
from datetime import timedelta

def generate_forecast(df, periods=30):
    """
    Generates a simple linear forecast for the next 'periods' days.
    """
    if 'Date' not in df or 'Revenue' not in df or len(df) < 2:
        return None
    
    # Prepare data for simple linear regression
    df = df.sort_values('Date')
    df['DayIndex'] = (df['Date'] - df['Date'].min()).dt.days
    
    x = df['DayIndex'].values
    y = df['Revenue'].values
    
    # Linear regression (slope and intercept)
    slope, intercept = np.polyfit(x, y, 1)
    
    # Generate future dates
    last_date = df['Date'].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, periods + 1)]
    future_day_indices = [(d - df['Date'].min()).days for d in future_dates]
    
    # Predict future revenue
    future_revenue = [max(0, slope * d + intercept) for d in future_day_indices]
    
    # Return as series
    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'Revenue': future_revenue
    })
    return forecast_df.set_index('Date')['Revenue']
