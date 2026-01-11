import pandas as pd
import os

HISTORY_FILE = "portfolio_history.csv"

def save_portfolio_history(metrics):
    if os.path.exists(HISTORY_FILE):
        history = pd.read_csv(HISTORY_FILE)
    else:
        history = pd.DataFrame()
    
    metrics["Timestamp"] = pd.Timestamp.now()
    history = pd.concat([history, pd.DataFrame([metrics])], ignore_index=True)
    history.to_csv(HISTORY_FILE, index=False)
