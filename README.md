# Professional Risk Radar MVP

[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-v1.26-orange)](https://streamlit.io/)

**Professional Risk Radar (PRR)** is a professional risk assessment tool for employees and specialists.  
It collects **public and professional data**, analyzes cases, career events, and conflicts of interest, and generates a **Risk Score** with **explainable factors** — helping companies make smarter, safer hiring and compliance decisions.  

---

## 🚀 Key Features

- **Rule-based Risk Score** for employees and specialists  
- **Risk Levels:** Suitable ✅ / Caution ⚠️ / High Risk 🚨  
- **Interactive Dashboard** with charts and career timeline  
- **Conflict Map:** visualize connections with high-risk companies or individuals  
- **PDF Report Generation** for internal use  
- **Explainable Factors:** textual explanations for each risk driver  

---

## 🎯 Intended Users

- HR, Legal, Compliance, Risk Departments  
- Companies that want to **minimize professional risk** and make informed hiring decisions  

---

## ⚡ How It Works

1. Upload a CSV with employee profiles  
2. Compute **Risk Score** and **Risk Level**  
3. View **career timeline** and **conflict map**  
4. Generate a **PDF report** for internal use  

---

## ⚠️ Disclaimer

- Only use **public and professional data**  
- Does **not evaluate personal or private information**  
- For **internal corporate use only**  


---

## 🗂️ Example CSV Structure

| **Name** | **Role** | **Company** | **Years_of_Experience** | **Cases_Total** | **Cases_Lost** | **Cases_High_Risk** | **Conflicts** | **Sanctioned_Connections** | **Career_Gaps** | **Risk_Factors_Notes** |
|----------|----------|-------------|------------------------|----------------|----------------|--------------------|---------------|----------------------------|-----------------|------------------------|
| Anna Kowalska | Lawyer | Law Firm A | 10 | 50 | 15 | 3 | 1 | 0 | 6 | No major issues |
| Piotr Nowak | Lawyer | Law Firm B | 8 | 40 | 18 | 6 | 2 | 1 | 0 | Some risky cases |


## 📊 Why Professional Risk Radar Matters

Hiring or working with risky employees can cost companies **hundreds of thousands to millions of euros per year**.  
Professional Risk Radar helps **prevent costly mistakes** by identifying high-risk profiles before they impact your business.

### Example Impact (Hypothetical)

| Metric | Before PRR | After PRR |
|--------|------------|-----------|
| High-Risk Employee Hires | 8 / year | 1 / year |
| Compliance Violations | 12 / year | 2 / year |
| Average Legal Costs | €500,000 / year | €100,000 / year |
| Time Spent on Manual Checks | 200 hours / year | 50 hours / year |

**Result:**  
- **~75% reduction** in high-risk hires  
- **~83% reduction** in compliance violations  
- **Significant cost savings** in legal fees and HR time  
- **Faster decision-making** and safer hiring  

---

### Why Companies Choose PRR

- Data-driven: uses **real case histories and professional metrics**  
- Explainable: every Risk Score comes with **clear factors**  
- Scalable: assess multiple roles, departments, or subsidiaries  
- Premium-ready: dashboard and PDF reports for **executive presentations**
## License
Create with MIT License - free to use


## 💻 Installation

```bash
git clone https://github.com/yourusername/Professional-Risk-Radar.git
cd Professional-Risk-Radar
pip install -r requirements.txt
streamlit run app.py
