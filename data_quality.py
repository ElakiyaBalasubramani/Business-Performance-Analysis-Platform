import pandas as pd

def audit_dataset(df):
    """
    Performs a quality check on the dataset.
    Returns a dictionary with audit results.
    """
    results = {
        "Total Rows": len(df),
        "Missing Values": df.isnull().sum().sum(),
        "Duplicate Rows": df.duplicated().sum(),
        "Column Info": []
    }
    
    for col in df.columns:
        col_type = str(df[col].dtype)
        missing = df[col].isnull().sum()
        unique = df[col].nunique()
        
        results["Column Info"].append({
            "Column": col,
            "Type": col_type,
            "Missing": missing,
            "Unique Values": unique
        })
        
    return results

def get_quality_score(results):
    """
    Calculates a simple quality score (0-100).
    """
    total_cells = results["Total Rows"] * len(results["Column Info"])
    if total_cells == 0:
        return 0
        
    missing_ratio = results["Missing Values"] / total_cells
    duplicate_ratio = results["Duplicate Rows"] / results["Total Rows"] if results["Total Rows"] > 0 else 0
    
    score = 100 * (1 - (missing_ratio + duplicate_ratio))
    return max(0, min(100, score))
