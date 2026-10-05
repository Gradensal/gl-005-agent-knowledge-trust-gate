# GL-005 Architecture

## Agent Knowledge Trust Gate

GL-005 explores a specific question in agent architecture:

> When an AI agent retrieves relevant information, is that evidence trustworthy enough to support the action the agent is preparing to take?

The prototype separates three concerns that are often collapsed into one workflow:

1. retrieval relevance;
2. evidence trust;
3. action authority.

GL-005 focuses on the second layer.

---

## System Boundary

The project does not perform semantic search, RAG, or autonomous agent execution.

It begins after knowledge has already been retrieved.

Its responsibility is to evaluate whether that knowledge satisfies an explicit evidence policy for the consequence of the proposed action.

```text
Upstream System
Retrieval / RAG / Search
        |
        v
+---------------------------+
| Retrieved Knowledge Item  |
+---------------------------+
        |
        v
+---------------------------+
| GL-005 TRUST GATE         |
|                           |
| Provenance                |
| Recency                   |
| Expertise                 |
| Corroboration             |
| Human Validation          |
| Conflict Detection        |
+---------------------------+
        |
        v
+---------------------------+
| Trust Score               |
| + Hard Policy Gates       |
| + Consequence Threshold   |
+---------------------------+
        |
        v
+----------+----------+----------+
|   USE    |  VERIFY  |  REJECT  |
+----------+----------+----------+
        |
        v
Audit / Agent Control Layer
```

---

## Core Components

### `KnowledgeItem`

Represents a retrieved piece of enterprise knowledge.

It contains the evidence statement, source information, and explicit trust metadata.

Current trust signals are:

- provenance;
- recency;
- expertise;
- corroboration;
- human validation;
- conflict detection.

The numeric trust values range from `0.0` to `1.0`.

These values are synthetic experimental inputs, not empirically validated trust measurements.

---

### `calculate_score()`

Produces a weighted aggregate trust score.

Current experimental weights are:

| Signal | Weight |
| --- | ---: |
| Provenance | 0.25 |
| Recency | 0.20 |
| Expertise | 0.20 |
| Corroboration | 0.20 |
| Human validation | 0.15 |

The weights sum to `1.00`.

The score is intentionally separated from the final policy decision.

A high score alone does not guarantee that evidence may be used.

---

### Hard Policy Gates

GL-005 includes deterministic rules that can override aggregate scoring.

Examples include:

- extremely weak provenance can reject evidence;
- high-consequence actions require stronger provenance;
- high-consequence actions require explicit human validation;
- detected conflicts require verification.

This protects the system from a failure mode in which several strong dimensions mathematically hide one critical weakness.

---

### Consequence Thresholds

The system currently models three consequence levels:

| Consequence | Trust Threshold |
| --- | ---: |
| LOW | 0.55 |
| MEDIUM | 0.70 |
| HIGH | 0.85 |

These thresholds are experimental.

They exist to test consequence-aware policy behavior rather than to prescribe real enterprise risk levels.

---

## Decision Model

The trust engine can return three outcomes.

### USE

The evidence satisfies the applicable trust requirements.

The downstream system may consider it eligible to support the proposed action.

### VERIFY

The evidence may be relevant or useful, but additional human or expert validation is required before relying on it for the proposed action.

### REJECT

The evidence falls below a minimum trust or provenance requirement and should not support the action.

---

## Decision Order

Policy evaluation occurs in a deliberate order:

```text
1. Detect conflict
       |
       +--> VERIFY

2. Check minimum provenance
       |
       +--> REJECT

3. Check minimum aggregate score
       |
       +--> REJECT

4. Apply high-consequence hard requirements
       |
       +--> VERIFY when unmet

5. Apply medium-consequence provenance requirement
       |
       +--> VERIFY when unmet

6. Compare trust score with consequence threshold
       |
       +--> VERIFY when below threshold

7. All applicable requirements satisfied
       |
       +--> USE
```

Ordering matters because some conditions must take precedence over the aggregate score.

---

## Experiment Architecture

The controlled experiment combines three evidence conditions with three consequence levels.

```text
3 Evidence Conditions
        x
3 Consequence Levels
        =
9 Policy Evaluations
```

Evidence conditions:

```text
Borderline / Unvalidated
Strong / Validated
Strong / Conflicting
```

Consequence levels:

```text
LOW
MEDIUM
HIGH
```

Every evaluation produces:

- scenario ID;
- knowledge ID;
- consequence level;
- trust score;
- required threshold;
- policy decision;
- decision reason;
- audit timestamp.

---

## Observed Results

The October 5, 2026 experiment produced the following deterministic policy outcomes:

| Evidence condition | LOW | MEDIUM | HIGH |
| --- | --- | --- | --- |
| Borderline / unvalidated | USE | VERIFY | VERIFY |
| Strong / validated | USE | USE | USE |
| Strong / conflicting | VERIFY | VERIFY | VERIFY |

Observed scores:

| Evidence condition | Score |
| --- | ---: |
| Borderline / unvalidated | 0.680 |
| Strong / validated | 0.957 |
| Strong / conflicting | 0.928 |

The strongest numerical score did not automatically determine authority.

The conflicting scenario scored `0.928` but still returned `VERIFY` at every consequence level because conflict detection is a hard policy condition.

This is an important property of the architecture.

---

## Audit Architecture

Every experiment evaluation is written to:

```text
traces/trust-experiment.jsonl
```

Each line is an independent JSON audit record.

Runtime traces are excluded from version control.

A deterministic experiment artifact is separately written to:

```text
results/experiment-results.json
```

The tracked result intentionally excludes runtime timestamps so that identical policy executions produce an identical version-controlled artifact.

---

## Deterministic vs Probabilistic Responsibilities

GL-005 deliberately contains no LLM in the core policy path.

The system is designed so that a future AI or retrieval component could propose or retrieve evidence while the final evidence-policy decision remains deterministic.

```text
Probabilistic Layer
Retrieve / interpret / reason
        |
        v
Deterministic Layer
Evaluate evidence policy
        |
        v
USE / VERIFY / REJECT
```

The architecture therefore remains operational even when no model provider is available.

---

## Security and Governance Considerations

The current project uses synthetic data only.

No customer information, credentials, API tokens, production policies, or confidential documents are required.

A production implementation would require substantially more work around:

- authenticated identities;
- source integrity;
- provenance verification;
- authorization;
- policy administration;
- tamper-resistant audit logs;
- validation authority;
- privacy;
- retention;
- incident response;
- policy versioning.

---

## Limitations

GL-005 is a research prototype.

Its current limitations include:

- synthetic scenarios;
- manually assigned trust metadata;
- experimentally chosen weights;
- experimentally chosen thresholds;
- no semantic retrieval;
- no automatic source verification;
- no cryptographic provenance;
- simplified conflict detection;
- no identity or authorization system;
- no production risk validation.

The prototype demonstrates architecture and policy behavior.

It does not establish an industry-standard trust model.

---

## Design Principle

The central design principle tested by GL-005 is:

> Retrieval relevance and decision authority should be treated as separate system concerns.

An AI system can retrieve highly relevant information while still lacking sufficient evidence to justify a consequential action.