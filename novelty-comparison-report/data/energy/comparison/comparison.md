# V1 vs V2 Energy Novelty Query Comparison

## V1 Decisions
- `forecast_aware_storage_dispatch`: novel=False
- `nonwires_demand_response_storage`: novel=False

## V1 Query Audit
- `forecast_aware_storage_dispatch`: queries=1, avg_query_len=14.0, energy_terms=microgrid, retrieved_titles=10

## V2 Decisions
- `counterfactual_restoration_probes`: novel=True (provisional)

## V2 Query Audit
- `energy_power_systems`: queries=1, avg_query_len=16.0, energy_terms=microgrid, retrieved_titles=2
