
import pandas as pd

def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file, encoding='latin1')
    elif file.name.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file)
    return None
