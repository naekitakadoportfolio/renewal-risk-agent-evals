"""Renewal risk scorer: transparent weighted rules, optional LLM explanation.
Rules make the score auditable; the LLM only writes the next-best-action text."""
import os
WEIGHTS = {"champion left": 3, "competitor": 3, "evaluating vendors": 2, "logins down": 2, "escalation": 2,
           "budget freeze": 2, "nps dropped": 1, "tickets up": 1, "late invoice": 1, "renewal in 30 days": 1,
           "positive": -1, "expanded": -2, "engaged": -1, "upsell": -1, "within sla": -1}

def score(signals):
    text = " | ".join(signals).lower()
    pts = sum(w for k, w in WEIGHTS.items() if k in text)
    level = "high" if pts >= 5 else "medium" if pts >= 2 else "low"
    return {"points": pts, "risk": level, "drivers": [k for k in WEIGHTS if k in text and WEIGHTS[k] > 0]}

def next_best_action(account, result):
    if result["risk"] == "high": return f"Escalate {account} to exec review this week; rebuild champion map."
    if result["risk"] == "medium": return f"Schedule a value review with {account} before renewal."
    return f"Keep {account} on standard cadence; explore expansion."
