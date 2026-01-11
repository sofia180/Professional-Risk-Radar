import os, json

def save_portfolio_history(metrics_dict, filename="history.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            history = json.load(f)
    else:
        history = []
    history.append(metrics_dict)
    with open(filename, "w") as f:
        json.dump(history, f)
