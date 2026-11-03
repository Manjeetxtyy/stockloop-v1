from dataclasses import dataclass
from datetime import datetime

@dataclass
class Approval:
    item: str
    source: str
    target: str
    quantity: int
    category: str
    status: str = "Pending"
    note: str = ""
    updated: str = ""

def decide(approval: Approval, action: str, note: str = "") -> Approval:
    if action not in {"Approve", "Reject", "Request review"}: raise ValueError("Unknown approval action")
    if action == "Approve" and approval.category == "Medicine":
        raise ValueError("Medicine transfers cannot be automatically authorised; request review instead.")
    approval.status, approval.note, approval.updated = action, note, datetime.now().isoformat(timespec="seconds")
    return approval

