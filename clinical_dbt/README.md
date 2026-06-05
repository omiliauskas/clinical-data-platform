# clinical_dbt

dbt project for the Clinical Data Platform. Transforms raw clinical data
(catalogued in AWS Glue, queried via Athena) into analytics-ready models.

## Layers

- **staging/** — The first transformation layer: one model per source, reading
  raw Glue tables with dbt `source()`. Flattens nested JSON, renames fields to
  snake_case, and standardizes types — turning messy raw data into a clean,
  typed foundation for the marts.

- **marts/** — Business logic and aggregation, built on the staging models with
  dbt `ref()`. `fct_trials_summary` combines the two trials staging models with a
  `UNION` (they share a schema; no shared key exists to join on) and aggregates
  trial counts and total enrollment by condition and overall status.

## Tests

Defined in `schema.yml` and run on every build — e.g. `not_null` and
`accepted_values`. These are the version-controlled equivalent of the manual
cross-source reconciliation checks behind a clinical database lock.

## Run

```bash
dbt run      # build models
dbt test     # run tests
dbt docs generate && dbt docs serve --port 8081   # lineage + docs
```

See the [root README](../README.md) for full architecture.