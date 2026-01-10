def calculate_risk(row):
    score = 0
    factors = []

    loss_ratio = row["Cases_Lost"] / max(row["Cases_Total"], 1)
    if loss_ratio > 0.3:
        score += 20
        factors.append("High loss ratio in past cases")

    if row["Cases_High_Risk"] >= 5:
        score += 25
        factors.append("Multiple high-risk cases")

    if row["Conflicts"] >= 2:
        score += 15
        factors.append("Conflict of interest indicators")

    if row["Sanctioned_Connections"] > 0:
        score += 30
        factors.append("Sanctioned connections detected")

    if row["Career_Gaps"] >= 6:
        score += 10
        factors.append("Significant career gaps")

    if score < 30:
        level = "LOW"
    elif score < 60:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return score, level, factors
