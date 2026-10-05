from pathlib import Path

from src.experiment import load_scenarios, run_experiment
from src.models import Consequence, TrustDecision

SCENARIOS = Path("scenarios/trust_scenarios.json")


def run_test_experiment(tmp_path: Path):
    scenarios = load_scenarios(SCENARIOS)

    return run_experiment(
        scenarios,
        trace_path=tmp_path / "trace.jsonl",
        results_path=tmp_path / "results.json",
    )


def test_experiment_produces_nine_decisions(tmp_path):
    records = run_test_experiment(tmp_path)

    assert len(records) == 9

    trace = tmp_path / "trace.jsonl"

    assert trace.exists()
    assert len(trace.read_text().splitlines()) == 9


def test_consequence_changes_borderline_decision(tmp_path):
    records = run_test_experiment(tmp_path)

    decisions = {
        (record.scenario_id, record.consequence): record.decision
        for record in records
    }

    assert decisions[
        ("borderline-unvalidated", Consequence.LOW)
    ] == TrustDecision.USE

    assert decisions[
        ("borderline-unvalidated", Consequence.MEDIUM)
    ] == TrustDecision.VERIFY

    assert decisions[
        ("borderline-unvalidated", Consequence.HIGH)
    ] == TrustDecision.VERIFY


def test_validated_and_conflicting_evidence(tmp_path):
    records = run_test_experiment(tmp_path)

    decisions = {
        (record.scenario_id, record.consequence): record.decision
        for record in records
    }

    for consequence in Consequence:
        assert decisions[
            ("strong-validated", consequence)
        ] == TrustDecision.USE

        assert decisions[
            ("strong-conflicting", consequence)
        ] == TrustDecision.VERIFY