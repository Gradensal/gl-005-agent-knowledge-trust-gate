from src.models import Consequence, KnowledgeItem, TrustDecision, TrustResult

WEIGHTS = {
    "provenance": 0.25,
    "recency": 0.20,
    "expertise": 0.20,
    "corroboration": 0.20,
    "human_validation": 0.15,
}


THRESHOLDS = {
    Consequence.LOW: 0.55,
    Consequence.MEDIUM: 0.70,
    Consequence.HIGH: 0.85,
}


MINIMUM_SCORE = 0.40
MINIMUM_PROVENANCE = 0.20
MEDIUM_PROVENANCE_FLOOR = 0.50
HIGH_PROVENANCE_FLOOR = 0.70


def calculate_score(item: KnowledgeItem) -> float:
    validation = 1.0 if item.human_validation else 0.0

    score = (
        item.provenance * WEIGHTS["provenance"]
        + item.recency * WEIGHTS["recency"]
        + item.expertise * WEIGHTS["expertise"]
        + item.corroboration * WEIGHTS["corroboration"]
        + validation * WEIGHTS["human_validation"]
    )

    return round(score, 3)


def evaluate(
    item: KnowledgeItem,
    consequence: Consequence,
) -> TrustResult:
    score = calculate_score(item)
    threshold = THRESHOLDS[consequence]

    if item.conflict_detected:
        return TrustResult(
            decision=TrustDecision.VERIFY,
            score=score,
            threshold=threshold,
            reason="Conflicting evidence requires human or expert validation.",
        )

    if item.provenance < MINIMUM_PROVENANCE:
        return TrustResult(
            decision=TrustDecision.REJECT,
            score=score,
            threshold=threshold,
            reason="Evidence provenance is below the minimum acceptable level.",
        )

    if score < MINIMUM_SCORE:
        return TrustResult(
            decision=TrustDecision.REJECT,
            score=score,
            threshold=threshold,
            reason="Evidence quality is below the minimum reliability floor.",
        )

    if (
        consequence == Consequence.HIGH
        and (
            item.provenance < HIGH_PROVENANCE_FLOOR
            or not item.human_validation
        )
    ):
        return TrustResult(
            decision=TrustDecision.VERIFY,
            score=score,
            threshold=threshold,
            reason=(
                "High-consequence actions require strong provenance "
                "and explicit human validation."
            ),
        )

    if (
        consequence == Consequence.MEDIUM
        and item.provenance < MEDIUM_PROVENANCE_FLOOR
    ):
        return TrustResult(
            decision=TrustDecision.VERIFY,
            score=score,
            threshold=threshold,
            reason=(
                "Evidence provenance is insufficient for "
                "a medium-consequence action."
            ),
        )

    if score < threshold:
        return TrustResult(
            decision=TrustDecision.VERIFY,
            score=score,
            threshold=threshold,
            reason=(
                "Evidence does not meet the required trust threshold "
                "for this action consequence."
            ),
        )

    return TrustResult(
        decision=TrustDecision.USE,
        score=score,
        threshold=threshold,
        reason="Evidence satisfies the required trust policy.",
    )