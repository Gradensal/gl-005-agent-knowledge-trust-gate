import json
from datetime import UTC, datetime
from pathlib import Path

from src.ledger import append_record
from src.models import Consequence, ExperimentRecord, TrustScenario
from src.trust_engine import evaluate

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SCENARIOS = PROJECT_ROOT / "scenarios" / "trust_scenarios.json"
DEFAULT_TRACE = PROJECT_ROOT / "traces" / "trust-experiment.jsonl"
DEFAULT_RESULTS = PROJECT_ROOT / "results" / "experiment-results.json"


def load_scenarios(
    path: Path = DEFAULT_SCENARIOS,
) -> list[TrustScenario]:
    payload = json.loads(path.read_text(encoding="utf-8"))

    return [
        TrustScenario.model_validate(item)
        for item in payload
    ]


def run_experiment(
    scenarios: list[TrustScenario],
    trace_path: Path = DEFAULT_TRACE,
    results_path: Path = DEFAULT_RESULTS,
) -> list[ExperimentRecord]:
    trace_path.unlink(missing_ok=True)

    records: list[ExperimentRecord] = []
    timestamp = datetime.now(UTC).isoformat()

    for scenario in scenarios:
        for consequence in Consequence:
            result = evaluate(
                scenario.knowledge,
                consequence,
            )

            record = ExperimentRecord(
                timestamp_utc=timestamp,
                scenario_id=scenario.scenario_id,
                knowledge_id=scenario.knowledge.knowledge_id,
                consequence=consequence,
                decision=result.decision,
                score=result.score,
                threshold=result.threshold,
                reason=result.reason,
            )

            append_record(record, trace_path)
            records.append(record)

    results_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    serialized = [
        record.model_dump(
            mode="json",
            exclude={"timestamp_utc"},
        )
        for record in records
    ]

    results_path.write_text(
        json.dumps(serialized, indent=2) + "\n",
        encoding="utf-8",
    )

    return records


def print_results(
    records: list[ExperimentRecord],
) -> None:
    print()
    print("GL-005 — Agent Knowledge Trust Gate")
    print("=" * 72)

    print(
        f"{'SCENARIO':<26}"
        f"{'CONSEQUENCE':<14}"
        f"{'SCORE':<10}"
        f"{'THRESHOLD':<12}"
        f"{'DECISION'}"
    )

    print("-" * 72)

    for record in records:
        print(
            f"{record.scenario_id:<26}"
            f"{record.consequence:<14}"
            f"{record.score:<10.3f}"
            f"{record.threshold:<12.2f}"
            f"{record.decision}"
        )

    print("=" * 72)
    print(f"Evaluations: {len(records)}")


def main() -> None:
    scenarios = load_scenarios()
    records = run_experiment(scenarios)
    print_results(records)


if __name__ == "__main__":
    main()