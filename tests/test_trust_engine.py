from src.models import Consequence, KnowledgeItem, TrustDecision
from src.trust_engine import evaluate


def strong_evidence() -> KnowledgeItem:
    return KnowledgeItem(
        knowledge_id="KB-001",
        statement="Refunds above $500 require manager approval.",
        source="Current finance policy",
        provenance=1.0,
        recency=0.95,
        expertise=0.95,
        corroboration=0.90,
        human_validation=True,
    )


def test_strong_validated_evidence_can_support_high_consequence_action():
    result = evaluate(
        strong_evidence(),
        Consequence.HIGH,
    )

    assert result.decision == TrustDecision.USE


def test_uncertain_evidence_requires_verification():
    item = KnowledgeItem(
        knowledge_id="KB-002",
        statement="Legacy systems may permit automatic refunds.",
        source="Unverified operations note",
        provenance=0.60,
        recency=0.60,
        expertise=0.60,
        corroboration=0.50,
        human_validation=False,
    )

    result = evaluate(
        item,
        Consequence.MEDIUM,
    )

    assert result.decision == TrustDecision.VERIFY


def test_low_quality_evidence_is_rejected():
    item = KnowledgeItem(
        knowledge_id="KB-003",
        statement="Old undocumented operating rule.",
        source="Unknown",
        provenance=0.10,
        recency=0.20,
        expertise=0.20,
        corroboration=0.10,
        human_validation=False,
    )

    result = evaluate(
        item,
        Consequence.LOW,
    )

    assert result.decision == TrustDecision.REJECT


def test_conflicting_evidence_requires_verification():
    item = strong_evidence().model_copy(
        update={"conflict_detected": True}
    )

    result = evaluate(
        item,
        Consequence.LOW,
    )

    assert result.decision == TrustDecision.VERIFY


def test_same_evidence_changes_with_consequence():
    item = KnowledgeItem(
        knowledge_id="KB-004",
        statement="Standard internal operating procedure.",
        source="Operations handbook",
        provenance=0.80,
        recency=0.80,
        expertise=0.80,
        corroboration=0.80,
        human_validation=False,
    )

    low = evaluate(
        item,
        Consequence.LOW,
    )

    high = evaluate(
        item,
        Consequence.HIGH,
    )

    assert low.decision == TrustDecision.USE
    assert high.decision == TrustDecision.VERIFY


def test_high_average_cannot_hide_weak_provenance():
    item = KnowledgeItem(
        knowledge_id="KB-005",
        statement="Highly polished but weakly sourced policy claim.",
        source="Unknown secondary document",
        provenance=0.30,
        recency=1.0,
        expertise=1.0,
        corroboration=1.0,
        human_validation=True,
    )

    result = evaluate(
        item,
        Consequence.HIGH,
    )

    assert result.decision == TrustDecision.VERIFY