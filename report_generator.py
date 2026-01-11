import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_report(df, col_name):
    # PDF
    pdf_file = f"report_{col_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    c = canvas.Canvas(pdf_file)
    c.drawString(50,800,f"Report for {col_name}")
    c.drawString(50,780,f"Mean: {df[col_name].mean():.4f}")
    c.drawString(50,760,f"Std: {df[col_name].std():.4f}")
    c.save()
    # XLSX
    xlsx_file = f"report_{col_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    df.to_excel(xlsx_file, index=False)
    return pdf_file
