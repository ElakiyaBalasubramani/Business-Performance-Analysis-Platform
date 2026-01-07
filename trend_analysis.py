
import pandas as pd

def revenue_trend(df):
    """
    Calculates revenue trend over time.
    Assumes 'Date' and 'Revenue' columns exist.
    """
    if 'Date' in df and 'Revenue' in df:
        df['Date'] = pd.to_datetime(df['Date'])
        return df.groupby('Date')['Revenue'].sum()
    return pd.Series()
