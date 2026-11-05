import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))
from evaluate import run
from scorer import score

def test_eval_meets_release_threshold():
    assert run()["passed"]

def test_champion_loss_is_high_risk():
    assert score(["champion left", "competitor demo", "logins down"])["risk"] == "high"
