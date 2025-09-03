from typing import List

def risk_band(glucose: float) -> str:
    if glucose < 70:
        return "hypo"
    if glucose > 180:
        return "hyper"
    return "in-range"
def alert_rules(pred_glucose: float, last_dose_u: float, last_glucose: float) -> List[str]:
    alerts = []
# Predicted bands
    band = risk_band(pred_glucose)
    if band == "hypo":
        alerts.append("⚠️ Predicted hypoglycemia risk")
    elif band == "hyper":
        alerts.append("⚠️ Predicted hyperglycemia risk")


# Simple overdose/underdose heuristics (placeholder; tune per clinician policy)
    if last_dose_u >= 10 and last_glucose < 100:
        alerts.append("❗ Possible overdose given low glucose and high recent dose")
    if last_dose_u <= 1 and last_glucose > 250:
        alerts.append("❗ Possible underdose given high glucose and very low dose")


    return alerts