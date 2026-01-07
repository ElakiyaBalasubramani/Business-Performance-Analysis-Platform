
import os
from openai import OpenAI

def generate_insights(kpis, trends, api_key=None):
    # Use provided key or environment variable
    final_key = api_key or os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
    client = OpenAI(api_key=final_key)
    
    prompt = f"""
    You are a strategic business consultant. Analyze the following business performance data:
    
    KEY METRICS:
    {kpis}
    
    TREND DATA (Revenue over time):
    {trends}
    
    Please provide:
    1. A summary of overall performance.
    2. Identification of any worrying trends or risks.
    3. Three actionable strategic recommendations to improve profitability or growth.
    4. A concise forward-looking forecast summary.
    
    Format the response in clean Markdown with bold headers.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating insights: {e}"
