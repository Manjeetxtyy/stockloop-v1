from __future__ import annotations
from datetime import date
import pandas as pd

def predict(row: pd.Series) -> dict:
    weeks = max(1, round(row["quantity"] / max(row["weekly_demand"], 1)))
    days_to_expiry = (row["expiry"] - date.today()).days if pd.notna(row["expiry"]) else None
    risk = "Low"
    reasons = [f"Current stock covers about {weeks} week(s) of simulated demand."]
    if days_to_expiry is not None and days_to_expiry < row["weekly_demand"] * 7:
        risk = "High"
        reasons.append(f"Simulated expiry is in {max(days_to_expiry, 0)} day(s), before expected usage.")
    elif weeks <= 2:
        risk = "Medium"
        reasons.append("Stock cover is below the two-week planning threshold.")
    else:
        reasons.append("No near-term simulated expiry or shortage signal was detected.")
    return {"risk": risk, "cover_weeks": weeks, "explanation": " ".join(reasons)}

def medicine_checks(row: pd.Series) -> dict:
    return {
        "batch": bool(row.get("batch")), "expiry": pd.notna(row.get("expiry")),
        "storage": bool(row.get("storage")), "traceability": row.get("traceability") == "Complete",
        "eligibility": bool(row.get("eligible")),
    }

def match_inventory(df: pd.DataFrame, item: str, source_site: str, target_site: str) -> list[dict]:
    source = df[(df.item == item) & (df.site == source_site)].iloc[0]
    targets = df[(df.item == item) & (df.site == target_site)]
    if targets.empty: return []
    target = targets.iloc[0]
    surplus = max(0, int(source.quantity - source.weekly_demand * 4))
    need = max(0, int(target.weekly_demand * 2 - target.quantity))
    checks = medicine_checks(source) if source.category == "Medicine" else {}
    return [{"item": item, "from": source_site, "to": target_site, "suggested_quantity": min(surplus, need),
             "reason": f"Source has {surplus} units above four-week cover; destination has {need} units of simulated two-week need.",
             "checks": checks, "eligible_to_request": surplus > 0 and need > 0 and (all(checks.values()) if checks else True)}]

