import json
from pathlib import Path

from src.models import ExperimentRecord


def append_record(
    record: ExperimentRecord,
    path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                record.model_dump(mode="json"),
                sort_keys=True,
            )
        )
        handle.write("\n")