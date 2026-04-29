# Energy V1 Smoke Summary

Date: 2026-04-27

Command:

```powershell
python -m energy_novelty_platform.cli init-run --config configs\autodl.smoke.json --out runs\autodl_smoke_v1_001 --only v1
```

Status: completed.

Outputs:

- `ideas_v1.json`
- `novelty_decisions_v1.json`
- `novelty_events_v1.jsonl`
- `query_audit_v1.json`

Notes:

- AutoDL.Art OpenAI-compatible API was used with `gpt-5.4`.
- Semantic Scholar was used without `S2_API_KEY`, matching the original AI-Scientist fallback behavior.
- Semantic Scholar returned 429 rate-limit responses and intermittent SSL EOF errors.
- The generated idea `nonwires_demand_response_storage` was marked `novel: false`.
- Query audit shows that the successful retrieved papers were mostly microgrid/model-predictive-control papers. This is useful evidence that energy-domain terminology coverage is still partial: the audit only detected `microgrid`, not stronger terms like `demand response`, `energy storage`, or `economic dispatch` in the successful logged query.

