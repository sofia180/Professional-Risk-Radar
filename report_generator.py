import pandas as pd
from fpdf import FPDF

def generate_report(df, main_col):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Financial Risk Report", ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Main metric: {main_col}", ln=True)
    pdf.ln(5)
    
    # Таблица первых 20 строк
    for col in df.columns:
        pdf.cell(40, 8, str(col), border=1)
    pdf.ln()
    
    for i in range(min(20, len(df))):
        for col in df.columns:
            pdf.cell(40, 8, str(df.iloc[i][col]), border=1)
        pdf.ln()
    
    report_file = "financial_risk_report.pdf"
    pdf.output(report_file)
    return report_file
