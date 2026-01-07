
def calculate_kpis(df):
    kpis = {
        "Total Revenue": df['Revenue'].sum(),
        "Average Revenue": df['Revenue'].mean(),
    }
    
    if 'Profit' in df:
        kpis["Total Profit"] = df['Profit'].sum()
        # Profit Margin
        if kpis["Total Revenue"] > 0:
            kpis["Profit Margin (%)"] = (kpis["Total Profit"] / kpis["Total Revenue"]) * 100
            
    if 'Expenses' in df:
        kpis["Total Expenses"] = df['Expenses'].sum()
        
    if 'Sales_Volume' in df and kpis["Total Revenue"] > 0:
        total_sales = df['Sales_Volume'].sum()
        if total_sales > 0:
            kpis["Revenue per Sale"] = kpis["Total Revenue"] / total_sales
            if "Total Profit" in kpis:
                kpis["Profit per Sale"] = kpis["Total Profit"] / total_sales
                
    return kpis
