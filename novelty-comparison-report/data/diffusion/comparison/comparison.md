# V1 vs V2 Novelty Query Comparison

## V1 Decisions
- `learning_rate_schedule`: novel=False
- `self_conditioned_mode_control`: novel=False

## V1 Query Audit
- `self_conditioned_mode_control`: queries=1, avg_query_len=9.0, retrieved_titles=8

## V2 Decisions
- `self_certified_guidance`: novel=True (provisional)

## V2 Query Audit
- `diffusion_models`: queries=2, avg_query_len=16.5, retrieved_titles=0
