from __future__ import annotations

from datetime import date, timedelta
import pandas as pd

SITES = [
    {"id": "north", "name": "Northbridge General", "region": "North", "capacity": 420},
    {"id": "riverside", "name": "Riverside Community", "region": "Central", "capacity": 180},
    {"id": "st_annes", "name": "St Anne's Specialist", "region": "South", "capacity": 260},
]

MEDICINES = [
    "Amoxicillin 500mg", "Metformin 500mg", "Atorvastatin 20mg", "Paracetamol 500mg", "Salbutamol 100mcg",
    "Warfarin 5mg", "Insulin glargine", "Omeprazole 20mg", "Furosemide 40mg", "Amlodipine 10mg",
    "Lidocaine 2%", "Cefalexin 500mg", "Morphine 10mg/ml", "Flucloxacillin 500mg", "Ondansetron 4mg",
    "Ramipril 5mg", "Enoxaparin 40mg", "Hydrocortisone 100mg", "Doxycycline 100mg", "Aspirin 75mg",
]
CONSUMABLES = [
    "Nitrile gloves (M)", "Nitrile gloves (L)", "Nitrile gloves (S)", "Surgical masks", "FFP3 respirators",
    "IV cannula 18G", "IV cannula 20G", "IV giving sets", "Syringes 10ml", "Syringes 20ml",
    "Needles 21G", "Alcohol wipes", "Gauze swabs", "Adhesive dressings", "Urinary catheters",
    "Blood collection tubes", "Specimen pots", "Tourniquets", "Suture packs", "Sterile drapes",
    "Theatre caps", "Shoe covers", "Nebuliser masks", "Oxygen tubing", "Wound drains", "ECG electrodes",
    "Pressure bags", "Sharps containers", "Thermal blankets", "Incontinence pads",
]

def inventory() -> pd.DataFrame:
    rows = []
    base = date.today()
    for site_i, site in enumerate(SITES):
        for item_i, item in enumerate(MEDICINES + CONSUMABLES):
            medicine = item in MEDICINES
            quantity = 18 + ((site_i * 17 + item_i * 11) % 90)
            weekly = 5 + ((site_i * 7 + item_i * 3) % 28)
            expiry = base + timedelta(days=35 + ((item_i * 13 + site_i * 19) % 440)) if medicine else None
            rows.append({
                "site_id": site["id"], "site": site["name"], "item": item,
                "category": "Medicine" if medicine else "Consumable", "quantity": quantity,
                "weekly_demand": weekly, "expiry": expiry, "storage": "2–8°C" if item_i % 7 == 0 and medicine else "Ambient",
                "batch": f"SIM-{site_i+1:02d}-{item_i+1:03d}", "traceability": "Complete" if item_i % 8 else "Review required",
                "eligible": item_i % 11 != 0,
            })
    return pd.DataFrame(rows)

