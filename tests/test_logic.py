import pandas as pd
from stockloop.data import inventory
from stockloop.logic import match_inventory, medicine_checks, predict
from stockloop.workflow import Approval, decide

def test_inventory_has_three_sites_and_50_items_per_site():
    df = inventory(); assert df.site.nunique() == 3; assert df.groupby("site").size().eq(50).all()
    assert (df.category == "Medicine").sum() == 60; assert (df.category == "Consumable").sum() == 90

def test_prediction_explains_risk():
    row = inventory().query("category == 'Medicine'").iloc[0]; result = predict(row)
    assert result["risk"] in {"Low", "Medium", "High"}; assert result["explanation"]

def test_medicine_checks_are_explicit():
    row = inventory().query("category == 'Medicine'").iloc[0]
    assert set(medicine_checks(row)) == {"batch", "expiry", "storage", "traceability", "eligibility"}

def test_matching_returns_check_gated_recommendation():
    df = inventory(); result = match_inventory(df, "Amoxicillin 500mg", "Northbridge General", "Riverside Community")
    assert result and "checks" in result[0]

def test_medicine_cannot_be_auto_approved():
    approval = Approval("Amoxicillin 500mg", "A", "B", 2, "Medicine")
    try: decide(approval, "Approve")
    except ValueError as exc: assert "cannot" in str(exc)
    else: assert False

