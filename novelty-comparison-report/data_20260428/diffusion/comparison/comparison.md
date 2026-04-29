# V1 vs V2 Novelty Query Comparison

## V1 Decisions
- `learning_rate_schedule`: novel=False
- `cluster_conditioned_diffusion`: novel=True

## V1 Query Audit
- `learning_rate_schedule`: queries=1, avg_query_len=8.0, retrieved_titles=10
- `cluster_conditioned_diffusion`: queries=2, avg_query_len=8.5, retrieved_titles=20

## V2 Decisions
- `diversity_adaptive_guidance`: novel=True (provisional)

## V2 Query Audit
- `diffusion_models`: queries=3, avg_query_len=17.3, retrieved_titles=0
