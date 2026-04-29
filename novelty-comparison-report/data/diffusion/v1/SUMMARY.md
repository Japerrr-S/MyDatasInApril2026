# Diffusion V1 Smoke Summary

Date: 2026-04-27

Command:

```powershell
python -m novelty_platform.cli init-run --config configs\autodl.smoke.json --out runs\autodl_smoke_v1_001 --only v1
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
- Semantic Scholar returned repeated 429 rate-limit responses, but one query for the generated idea eventually returned results.
- The generated idea `self_conditioned_mode_control` was marked `novel: false`.
- Query audit found strong related work, including `Why Are Conditional Generative Models Better Than Unconditional Ones?`, which discusses self-conditioned diffusion models with k-means clustered conditions.

