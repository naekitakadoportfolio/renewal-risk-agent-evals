"""Evaluation harness: runs the scorer on a labeled set and reports accuracy, a confusion matrix,
and every miss, so changes to weights can be tested before release."""
import json, sys
from collections import Counter
from pathlib import Path
from scorer import score, next_best_action

def run(threshold=0.8):
    cases = json.loads((Path(__file__).parent.parent / "data/eval_set.json").read_text())
    confusion, misses = Counter(), []
    for c in cases:
        r = score(c["signals"]); confusion[(c["expected"], r["risk"])] += 1
        if r["risk"] != c["expected"]: misses.append({"account": c["account"], "expected": c["expected"], "got": r["risk"], "points": r["points"]})
    acc = sum(v for (e, g), v in confusion.items() if e == g) / len(cases)
    report = {"cases": len(cases), "accuracy": round(acc, 2), "passed": acc >= threshold,
              "confusion": {f"{e}->{g}": v for (e, g), v in confusion.items()}, "misses": misses,
              "sample_action": next_best_action(cases[0]["account"], score(cases[0]["signals"]))}
    return report

if __name__ == "__main__":
    rep = run(); print(json.dumps(rep, indent=2)); sys.exit(0 if rep["passed"] else 1)
