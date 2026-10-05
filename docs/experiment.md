# GL-005 Experiment

## Research Question

Should the evidence threshold supporting an AI agent action increase as the consequence of that action increases?

## Hypothesis

Evidence that is sufficient for a low-consequence action may be insufficient for a higher-consequence action.

Conflicting evidence should trigger verification even when its individual trust signals are otherwise strong.

## Method

Three synthetic enterprise knowledge conditions are evaluated against three action-consequence levels:

1. LOW
2. MEDIUM
3. HIGH

This produces nine controlled policy evaluations.

## Evidence Conditions

### Borderline / Unvalidated

Reasonably strong evidence without explicit human validation.

This scenario is designed to test whether evidence that appears sufficiently reliable for a low-consequence action should still require additional verification when the consequence increases.

### Strong / Validated

Recent, authoritative, corroborated evidence with explicit human validation.

This scenario represents the strongest evidence condition in the experiment.

### Strong / Conflicting

High-quality evidence for which another credible source presents a conflicting rule.

This scenario tests whether detected disagreement should override an otherwise strong trust score.

## Independent Variable

The action consequence level:

- LOW
- MEDIUM
- HIGH

## Evidence Variables

Each knowledge item contains explicit trust signals:

- provenance
- recency
- expertise
- corroboration
- human validation
- conflict detection

## Dependent Variable

The policy engine produces one of three decisions:

- USE
- VERIFY
- REJECT

### USE

The available evidence satisfies the policy requirements for the proposed consequence level.

### VERIFY

The evidence may be useful, but additional human or expert validation is required before the agent should rely on it for the proposed action.

### REJECT

The evidence falls below a minimum reliability or provenance requirement and should not support the action.

## Experimental Architecture

The experiment separates evidence quality from action consequence.

```text
Knowledge Item
      |
      v
Trust Signals
      |
      v
Trust Score
      |
      +----------------------+
      |                      |
      v                      v
Hard Policy Gates      Consequence Threshold
      |                      |
      +----------+-----------+
                 |
                 v
        USE / VERIFY / REJECT
                 |
                 v
           Audit Record
```

The same evidence can therefore produce different outcomes depending on the consequence of the proposed action.

## Policy Design

The current prototype uses both:

1. weighted trust scoring; and
2. deterministic hard policy gates.

Weighted scoring combines:

- provenance
- recency
- expertise
- corroboration
- human validation

Hard policy rules prevent a strong aggregate score from hiding certain weaknesses.

For example, high-consequence actions require stronger provenance and explicit human validation.

Conflicting evidence always requires verification.

## Important Constraint

The trust weights and thresholds used in GL-005 are experimental design choices.

They are not derived from Stack Overflow, an industry standard, or empirical safety research.

The project tests an architecture and policy concept rather than claiming to establish optimal trust thresholds.

The synthetic scenarios are designed to make policy behavior observable and reproducible.

They should not be interpreted as validated enterprise risk policies.

## Reproducibility

From the repository root, activate the Python virtual environment if necessary:

```bash
source .venv/bin/activate
```

Run the automated quality checks:

```bash
ruff check .
pytest
```

Run the experiment:

```bash
python -m src.experiment
```

The experiment evaluates:

```text
3 evidence conditions
x
3 consequence levels
=
9 deterministic evaluations
```

## Generated Artifacts

The experiment creates:

```text
traces/trust-experiment.jsonl
results/experiment-results.json
```

### Audit Trace

`traces/trust-experiment.jsonl`

The JSONL trace records every individual policy decision as an independent machine-readable record.

The trace is operational output and is intentionally excluded from version control.

### Experiment Results

`results/experiment-results.json`

The JSON results file preserves the synthetic experiment outcomes in a format suitable for:

- repository review;
- reproducibility;
- later analysis;
- comparison between future policy versions;
- portfolio evidence.

## What the Experiment Tests

The experiment is designed to test four architectural behaviors.

### 1. Consequence-Aware Trust

The same evidence should not necessarily receive identical treatment for every proposed action.

A low-consequence use may be permitted while a high-consequence use requires verification.

### 2. Human Validation

Explicit validation becomes increasingly important as consequences rise.

### 3. Conflict Handling

Strong evidence should not automatically proceed when credible conflicting information has been detected.

### 4. Hard Constraints

Aggregate scores should not automatically override critical trust requirements such as provenance.

## What the Experiment Does Not Prove

GL-005 does not prove:

- that the current numerical thresholds are optimal;
- that the current weights reflect real organizational risk;
- that five trust signals are sufficient for production systems;
- that human validation guarantees correctness;
- that the policy architecture is appropriate for every domain;
- that the system can automatically verify whether a source is truthful;
- that this prototype reproduces Stack Overflow Stack Internal.

The experiment demonstrates a design pattern:

> Evidence quality and action consequence can be treated as separate inputs to an explicit agent policy decision.

## Expected Learning

The experiment should help clarify the difference between:

```text
retrieval relevance
```

and:

```text
decision authority
```

A system can successfully retrieve information while still lacking sufficient evidence to justify a consequential action.

## Next Research Questions

Future iterations could investigate:

- trust decay over time;
- evidence bundles containing multiple sources;
- source-authority hierarchies;
- provenance graphs;
- signed human validation;
- disagreement between experts;
- domain-specific consequence policies;
- policy precedence;
- dynamically changing evidence;
- integration with agent delegation controls;
- integration with agent observability and audit systems.

## Prototype Status

GL-005 is a research prototype.

It is designed to make evidence-policy behavior inspectable, testable, and explainable.

It is not production-ready enterprise governance software.