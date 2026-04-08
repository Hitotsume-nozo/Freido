# Freido — Forensic Fraud Investigation (OpenEnv)

Freido is an OpenEnv environment that simulates a real-world task: **forensic corporate fraud investigation**.

An agent is dropped into an internal records “data room” after a whistleblower tip. The agent must:

1. examine documents,
2. identify and flag key evidence,
3. attribute responsibility (mastermind / accomplice / witness / reluctant participant),
4. build a timeline,
5. submit a structured report.

This environment is designed to measure **evidence-grounded, multi-document reasoning**—not just classification.

---

## Why this benchmark is valuable (what it measures)

Most agent benchmarks reward short, clean tasks. Real investigations are the opposite: noisy, multi-source, ambiguous, and high-stakes. Freido targets capabilities that matter in compliance / audit / due diligence settings:

- **Multi-document reasoning** under a step budget
- **Cross-source contradiction detection** (emails vs calendars vs external registry vs financials)
- **Attribution under uncertainty** (perpetrator vs pressured witness)
- **Precision, not just recall**: false accusations and evidence spam are penalized
- **Deterministic grading** with partial credit and reproducible scores

---

## Tasks (3 scenarios, easy → medium → hard)

All tasks have deterministic gold labels + graders and return scores in \[0, 1\].

### Task 1 (Easy): The Expense Report

A sales manager submits suspicious “client dinner” expenses. The agent must cross-reference:

- expense reports
- restaurant closure info
- travel calendar / CRM notes
- client replies

**Max steps:** 20

### Task 2 (Medium): The Vendor Kickback

Procurement repeatedly awards overpriced contracts to a vendor connected to an employee via a hidden relationship (alias / registry evidence).

**Max steps:** 30

### Task 3 (Hard): The Quarter That Never Was

Systematic **revenue fabrication** ahead of fundraising using shell customers + unsupported recognition across multiple departments.

**Max steps:** 40

---

## Environment API (OpenEnv-style)

The environment is served via a Dockerized FastAPI app (HF Space).

Endpoints:

- `GET /` health
- `GET /tasks` task metadata
- `POST /reset` start an episode (**body optional**, validator-friendly)
- `POST /step` apply an action
- `GET /state?session_id=...` debug state

Example:

```bash
curl -X POST https://YOUR_SPACE.hf.space/reset
```

---

## Action space (high level)

Agents act through typed actions (Pydantic models in `models.py`):

- `examine_document(document_id)`
- `search_records(query)`
- `cross_reference(document_ids=[...])`
- `flag_evidence(document_id, evidence_reason)`
- `identify_suspect(person_name, person_role, evidence_ids, evidence_reason)`
- `establish_timeline(timeline_events=[...])`
- `submit_report(findings={scheme_type, summary})`

---

## Observation space (high level)

Observations include:

- scenario + whistleblower tip
- `available_sources` (document index with IDs + metadata)
- last document content / search results / cross-reference output
- current evidence board (flagged evidence)
- suspects board (identified suspects + roles)
- timeline state
- step counters + last error/result

---

## Reward / grading (what drives the score)

The grader is deterministic and rewards structured investigation:

**Positive credit (partial, throughout the episode):**

- correct scheme type
- correct perpetrator identification (with role)
- key evidence flagged
- coherent timeline

**Penalties:**

- false accusations (especially innocents marked as mastermind/accomplice)
- overinclusive / irrelevant evidence flagging

A key design detail: **penalties are applied after clamping the positive score**, so penalties are not “hidden” when the positive total exceeds 1.0.

---

## Baseline inference (validator-compatible)

`inference.py` is a reproducible baseline that:

- uses the OpenAI client
- uses `API_BASE_URL` + `API_KEY` injected by the evaluator (LiteLLM proxy)
- prints machine-parseable logs:
  - `[START] task=...`
  - `[STEP] ...`
  - `[END] task=... score=... steps=...`
- reports final task scores strictly within **(0, 1)** for validator requirements

Local example (your own provider):

```bash
export API_BASE_URL="https://api.groq.com/openai/v1"
export API_KEY="YOUR_KEY"
export MODEL_NAME="moonshotai/kimi-k2-instruct-0905"
python inference.py
```

If proxy vars are missing, the script falls back to a deterministic mode (still emits structured logs).

---

## Benchmark audit (validity evidence)

This repo includes two audit tools to demonstrate benchmark validity and exploit resistance.

### 1) `benchmark_audit.py` — calibration & sanity checks

Runs multiple policies (oracle, random, scheme-only, false-accusation, overinclusive) and outputs:

- `benchmark_audit_results.json`
- `BENCHMARK_AUDIT.md`

Run:

```bash
python benchmark_audit.py
```

- Check them out at Benchmark_audit

Example audit summary (typical):

- `oracle_case` ≈ near ceiling (solvable; grader rewards correct behavior)
- `scheme_only_submit` low (naming the scheme alone is not enough)
- `random_policy` low (not trivially exploitable)
- `false_accusation_case` measurably lower than oracle (precision matters)
- `overinclusive_case` much lower than oracle (evidence spam is penalized)

### 2) `redaudit.py` — red-team exploit probes

Runs adversarial probes like:

- flagging evidence without examination
- accusing suspects without evidence
- evidence spam
- metadata-only submit

and outputs a Markdown report for review.

Run:

```bash
python redaudit.py
```

These audits are included specifically to show:

- the environment is not a toy,
- the grader has meaningful incentives,
- exploit attempts are measurable and can be hardened against.
- You can view them in export audit

---

## Run locally

### Python (dev)

```bash
pip install -r requirements.txt
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### Docker

```bash
docker build -t freido .
docker run -p 7860:7860 freido
```

---

## Repository layout

```text
.
├── environment.py
├── graders.py
├── models.py
├── inference.py
├── openenv.yaml
├── server/
│   ├── app.py
│   └── __init__.py
├── tasks/
│   ├── easy.py
│   ├── medium.py
│   └── hard.py
├── benchmark_audit.py
├── redaudit.py
├── pyproject.toml
├── uv.lock
├── Dockerfile
└── requirements.txt
```

---

## Notes

- Freido is synthetic by design (fully deterministic, reproducible), but the mechanics mirror real investigative patterns:
  - expense fraud
  - procurement kickbacks
  - revenue fabrication
- The included audit scripts serve as “proof of work” that the benchmark:
  - differentiates naive vs structured behavior
  - penalizes false accusations and overinclusive evidence collection
  - is not easily exploitable by random strategies

```

```
