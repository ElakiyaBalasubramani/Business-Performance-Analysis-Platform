import pandas as pd
import numpy as np

def detect_anomalies(df, column='Revenue', threshold=2.0):
    """
    Detects anomalies in a specific column using Z-score method.
    Returns a series of boolean masks where True indicates an anomaly.
    """
    if column not in df.columns or len(df) < 3:
        return pd.Series([False] * len(df), index=df.index)
        
    data = df[column]
    mean = data.mean()
    std = data.std()
    
    if std == 0:
        return pd.Series([False] * len(df), index=df.index)
        
    z_scores = np.abs((data - mean) / std)
    return z_scores > threshold

def get_anomaly_summary(df, column='Revenue', threshold=2.0):
    """
    Returns a dataframe of rows that are considered anomalies.
    """
    is_anomaly = detect_anomalies(df, column, threshold)
    return df[is_anomaly].copy()
