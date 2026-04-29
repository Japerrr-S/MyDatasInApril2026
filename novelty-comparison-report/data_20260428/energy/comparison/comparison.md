# V1 vs V2 Energy Novelty Query Comparison

## V1 Decisions
- `forecast_aware_storage_dispatch`: novel=False
- `adaptive_peak_shaving_dispatch`: novel=False

## V1 Query Audit
- `adaptive_peak_shaving_dispatch`: queries=1, avg_query_len=12.0, energy_terms=none, retrieved_titles=1

## V2 Decisions
- `conformal_opf_reserve_activation`: novel=True (provisional)

## V2 Query Audit
- `energy_power_systems`: queries=3, avg_query_len=20.0, energy_terms=demand response, electricity market, frequency regulation, n-1 security, optimal power flow, renewable integration, retrieved_titles=4
