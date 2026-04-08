# Benchmark Audit

This document audits the forensic fraud investigation environment for benchmark validity, exploit resistance, and score calibration.

## Policies evaluated

- **scheme_only_submit**: immediately submits the correct scheme type without gathering evidence
- **read_only_then_submit**: examines gold-relevant documents but does not flag evidence or build a case
- **submitted_baseline_fallback**: deterministic task-aware baseline report used by the submitted inference fallback path
- **oracle_case**: uses gold evidence, gold perpetrators, and a coherent timeline
- **false_accusation_case**: oracle-like case plus one intentionally wrong accusation
- **overinclusive_case**: oracle-like case plus irrelevant evidence and/or an overinclusive accusation
- **random_policy**: seeded random action policy averaged over 5 runs

## Score table

| Policy | Easy | Medium | Hard | Average |
|---|---:|---:|---:|---:|
| false_accusation_case | 0.93 | 0.92 | 0.89 | 0.9133 |
| oracle_case | 1.0 | 1.0 | 0.99 | 0.9967 |
| overinclusive_case | 0.44 | 0.46 | 0.55 | 0.4833 |
| random_policy | 0.096 | 0.086 | 0.0484 | 0.0768 |
| read_only_then_submit | 0.2 | 0.15 | 0.1 | 0.15 |
| scheme_only_submit | 0.2 | 0.15 | 0.1 | 0.15 |
| submitted_baseline_fallback | 1.0 | 0.85 | 0.62 | 0.8233 |

## Key findings

- **Scheme-only submit** averages **0.15**, showing that guessing the fraud type without evidence is not enough.
- **Read-only then submit** averages **0.15**, demonstrating that document inspection alone is insufficient unless the agent structures findings.
- **Oracle case** averages **0.9967**, showing the tasks are solvable and the grader rewards correct evidence-grounded behavior.
- Adding a **false accusation** drops the average from **0.9967** to **0.9133**, indicating that over-aggressive accusations are meaningfully penalized.
- **Overinclusive evidence / accusation behavior** scores **0.4833** vs oracle **0.9967**, suggesting the benchmark values precision over shotgun evidence collection.
- **Random policy mean** averages **0.0768**, showing that the environment is not trivially exploitable by unguided behavior.

## Interpretation

The audit is intended to show that the benchmark rewards structured, evidence-grounded investigation while penalizing under-specified, random, or overly aggressive case-building behavior.

In particular, the gap between naive and oracle-like policies indicates that the environment is non-trivial, while the false-accusation and overinclusive cases probe whether the benchmark values precision and careful attribution.
