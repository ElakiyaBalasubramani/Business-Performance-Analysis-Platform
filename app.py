
import streamlit as st
import pandas as pd
import os
import numpy as np
from utils.data_loader import load_data
from analytics.kpi_engine import calculate_kpis
from analytics.trend_analysis import revenue_trend
from analytics.forecast_engine import generate_forecast
from analytics.anomaly_detector import get_anomaly_summary, detect_anomalies
from utils.data_quality import audit_dataset, get_quality_score
from llm.insight_generator import generate_insights

st.set_page_config(page_title="Nexus BI - Performance Platform", layout="wide")

# Premium UI Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    h1, h2, h3 {
        color: #1e293b;
        font-family: 'Inter', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Nexus BI: Strategic Performance Platform")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    demo_mode = st.toggle("🚀 Demo Mode (Mock AI)", value=True, help="Enable this to see simulated insights without an API key.")
    
    with st.expander("🔑 OpenAI API Key Settings"):
        env_key = os.getenv("OPENAI_API_KEY")
        api_key_input = st.text_input(
            "Enter Key", 
            value=env_key if env_key else "",
            type="password",
            help="Required for real strategic analysis."
        )
    
    if not api_key_input and not demo_mode:
        st.warning("⚠️ Please provide a key or enable Demo Mode.")
    
    st.divider()
    st.header("📂 Data Source")
    file = st.file_uploader("Upload Business Dataset", type=["csv", "xlsx"])

if file:
    df = load_data(file)
    if 'Date' in df:
        df['Date'] = pd.to_datetime(df['Date'])
    
    # Sidebar Filters
    with st.sidebar:
        st.divider()
        st.header("🔍 Filters")
        if 'Date' in df:
            min_date = df['Date'].min().to_pydatetime()
            max_date = df['Date'].max().to_pydatetime()
            date_range = st.date_input("Select Date Range", value=(min_date, max_date))
            
            # Apply Date Filter
            if len(date_range) == 2:
                start_date, end_date = date_range
                df = df[(df['Date'] >= pd.Timestamp(start_date)) & (df['Date'] <= pd.Timestamp(end_date))]
        
        st.divider()
        st.header("📈 Visualization")
        agg_level = st.selectbox("Aggregation Level", ["Daily", "Weekly", "Monthly"], index=0)

    # Apply Aggregation
    if agg_level == "Weekly":
        df = df.resample('W', on='Date').sum().reset_index()
    elif agg_level == "Monthly":
        df = df.resample('M', on='Date').sum().reset_index()

    # Create Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Performance Dashboard", "⚠️ Anomaly Analysis", "🏥 Data Health Audit"])

    with tab1:
        st.subheader("📊 Key Performance Indicators")
        kpis = calculate_kpis(df)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Revenue", f"${kpis.get('Total Revenue', 0):,.2f}")
        m2.metric("Total Profit", f"${kpis.get('Total Profit', 0):,.2f}")
        m3.metric("Profit Margin", f"{kpis.get('Profit Margin (%)', 0):.1f}%")
        m4.metric("Avg. Revenue", f"${kpis.get('Average Revenue', 0):,.2f}")

        # Unit Economics metrics
        u1, u2 = st.columns(2)
        if "Revenue per Sale" in kpis:
            u1.metric("Revenue per Sale", f"${kpis['Revenue per Sale']:.2f}", help="Average revenue generated per individual sale/unit.")
        if "Profit per Sale" in kpis:
            u2.metric("Profit per Sale", f"${kpis['Profit per Sale']:.2f}", help="Average profit kept from each individual sale.")

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Revenue Trend")
            trend = revenue_trend(df)
            st.line_chart(trend)

        with col2:
            st.subheader("⚖️ Revenue vs Expenses")
            if 'Revenue' in df and 'Expenses' in df:
                comparison_df = df.groupby('Date')[['Revenue', 'Expenses']].sum()
                st.bar_chart(comparison_df)

        # Simulator & Forecasting
        st.divider()
        s1, s2 = st.columns(2)
        
        with s1:
            st.subheader("🎮 What-If Scenario Simulator")
            st.write("Simulate changes to see the impact on Profit.")
            exp_delta = st.slider("Expense Reduction (%)", 0, 50, 0)
            sales_delta = st.slider("Sales Growth (%)", 0, 100, 0)
            
            sim_revenue = kpis.get('Total Revenue', 0) * (1 + sales_delta/100)
            sim_expenses = kpis.get('Total Expenses', 0) * (1 - exp_delta/100)
            sim_profit = sim_revenue - sim_expenses
            
            c1, c2 = st.columns(2)
            actual_profit = kpis.get('Total Profit', 0)
            c1.metric("Simulated Profit", f"${sim_profit:,.2f}", delta=f"${sim_profit - actual_profit:,.2f}")
            c2.metric("Simulated Margin", f"{(sim_profit/sim_revenue*100):.1f}%" if sim_revenue > 0 else "0%")

        with s2:
            st.subheader("🔮 30-Day Revenue Forecast")
            forecast = generate_forecast(df)
            if forecast is not None:
                # Combine historical trend and forecast
                hist_trend = df.groupby('Date')['Revenue'].sum()
                combined = pd.concat([hist_trend, forecast])
                st.line_chart(combined)
                st.caption("Historical data + Blue line projection based on linear regression.")
            else:
                st.warning("Not enough data to generate a forecast.")

        st.divider()
        st.subheader("🧠 Strategic LLM Insights")
        
        if st.button("Generate Strategic Analysis"):
            if demo_mode:
                st.info("Showing Mock Insights (Demo Mode)")
                mock_insights = f"""
                **Strategic Analysis:**
                - **Growth**: Revenue has shown consistent performance with a profit margin of {kpis.get('Profit Margin (%)', 0):.1f}%.
                - **Efficiency**: Expenses are tracked closely; further reduction in fixed costs could boost overall margin.
                - **Forecast**: Based on current trends, the next quarter looks promising if current sales volume is maintained.
                """
                st.write(mock_insights)
            elif api_key_input:
                with st.spinner("AI is analyzing your business data..."):
                    insights = generate_insights(kpis, trend.to_dict(), api_key=api_key_input)
                    st.markdown(insights)
            else:
                st.warning("Please provide an OpenAI API key in the sidebar or enable Demo Mode.")

    with tab2:
        st.subheader("⚠️ Intelligence Alert: Anomaly Detection")
        st.write("Automatically identifying statistical outliers in your business metrics.")
        
        anom_col1, anom_col2 = st.columns([2, 1])
        
        target_metric = anom_col2.selectbox("Select Metric to Audit", ["Revenue", "Expenses", "Profit", "Sales_Volume"])
        z_thresh = anom_col2.slider("Sensitivity (Z-Score)", 1.0, 4.0, 2.0, help="Lower = more sensitive, Higher = only major anomalies.")
        
        anomalies = get_anomaly_summary(df, column=target_metric, threshold=z_thresh)
        
        with anom_col1:
            if not anomalies.empty:
                st.warning(f"🚨 Found {len(anomalies)} anomalies in {target_metric}!")
                st.scatter_chart(df, x='Date', y=target_metric, color='Profit', size=detect_anomalies(df, target_metric, z_thresh))
                st.caption(f"Points sized by anomaly status. Larger points = higher deviation in {target_metric}.")
            else:
                st.success(f"✅ No significant anomalies detected in {target_metric} at this sensitivity level.")

        if not anomalies.empty:
            with st.expander("🔍 Detailed Anomaly Report"):
                st.dataframe(anomalies.style.apply(lambda x: ['background-color: #ffcccc' if x.name in anomalies.index else '' for _ in x], axis=1), use_container_width=True)

        st.divider()
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.subheader("🔗 Factor Correlation")
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                corr = numeric_df.corr()
                st.write("Correlation between key business factors:")
                st.dataframe(corr.style.background_gradient(cmap='RdYlGn'), use_container_width=True)
                
        with c2:
            st.subheader("📦 Sales Volume vs Revenue")
            if 'Sales_Volume' in df and 'Revenue' in df:
                st.scatter_chart(df, x='Sales_Volume', y='Revenue', color='Profit')

    with tab3:
        st.subheader("🏥 Data Infrastructure Audit")
        st.write("Analyzing the integrity and quality of your uploaded business dataset.")
        
        audit_results = audit_dataset(df)
        q_score = get_quality_score(audit_results)
        
        # Quality Score Gauge
        c1, c2, c3 = st.columns(3)
        c1.metric("Data Quality Score", f"{q_score:.1f}%")
        c2.metric("Missing Cells", audit_results["Missing Values"])
        c3.metric("Duplicate Rows", audit_results["Duplicate Rows"])
        
        if q_score > 90:
            st.success("🌟 Your data is in excellent shape!")
        elif q_score > 70:
            st.info("ℹ️ Your data is healthy, but has minor gaps.")
        else:
            st.error("⚠️ Data quality issues detected. Please clean your dataset for better insights.")
            
        st.subheader("📋 Column Specifications")
        st.table(pd.DataFrame(audit_results["Column Info"]))

    with st.expander("👀 Raw Data View"): 
        st.dataframe(df, use_container_width=True)
        # Export Button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name='filtered_business_data.csv',
            mime='text/csv',
        )
else:
    st.info("Please upload a CSV or Excel file to begin your analysis.")
