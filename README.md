# Clinical Data Platform

An end-to-end **ELT pipeline** that ingests public clinical-trial and adverse-event data, lands it in **AWS S3**, and transforms it with **dbt** into analytics-ready models — orchestrated with **Airflow**, queried through **Athena**, and provisioned with **Terraform**.

> Built as a hands-on data-engineering project. It mirrors a pattern from my background in clinical data management: the cross-source reconciliation and quality checks I used to write by hand are now version-controlled **dbt tests** that run automatically on every build.

---

## Architecture

```mermaid
flowchart LR
    subgraph Ingestion["Ingestion · Python + Airflow"]
        API1[ClinicalTrials.gov API]
        API2[OpenFDA API]
        FET[Python fetchers]
        API1 --> FET
        API2 --> FET
    end

    subgraph Lake["AWS S3 · Data Lake"]
        RAW[("raw/ · JSON<br/>immutable copy")]
        STG[("staging/ · Parquet<br/>query-ready")]
    end

    FET -->|archive raw| RAW
    FET -->|convert| STG

    subgraph Query["Catalog + Query"]
        CRAWL[Glue Crawler]
        CAT[Glue Data Catalog]
        ATH[Athena]
        STG --> CRAWL --> CAT --> ATH
    end

    subgraph Transform["Transformation · dbt"]
        DSTG[staging models]
        MART[marts · fct_trials_summary]
        ATH --> DSTG --> MART
    end
```

*Airflow orchestrates the ingestion DAG (fan-in to the Glue crawler). Terraform provisions all AWS infrastructure. GitHub Actions runs CI on every push.*

**Flow:** Python fetchers pull data from the ClinicalTrials.gov and OpenFDA APIs. Each raw response is archived as **JSON in S3 `raw/`** (an immutable, replayable copy), then converted to **Parquet and landed in S3 `staging/`**. A **Glue crawler** catalogs `staging/` into the Glue Data Catalog, so **Athena** can query it via schema-on-read. **dbt** then models the data: a **staging** layer cleans and standardizes each source, and a **marts** layer applies business logic and aggregation into analytics-ready tables.

---

## Tech stack

| Layer | Tooling |
|---|---|
| Ingestion | Python, `requests`, `boto3` |
| Storage / Lake | AWS S3 (raw JSON + staging Parquet) |
| Catalog / Query | AWS Glue (crawler + Data Catalog), Athena |
| Transformation | dbt (staging → marts, tests, docs/lineage) |
| Orchestration | Apache Airflow (Dockerized) |
| Infrastructure | Terraform (S3, versioning, Glue role/DB/crawler) |
| CI | GitHub Actions |

---

## How it works

**Medallion layout in S3.** Raw and transformed data live under separate prefixes so they never collide:
- **`raw/` (JSON)** — write-once, immutable. This is the source of truth. If a downstream transform breaks or a schema changes, the pipeline can be reprocessed from here without re-calling the APIs (which rate-limit and change over time).
- **`staging/` (Parquet)** — columnar, query-ready. This is the *only* prefix the Glue crawler scans, which keeps the catalog clean (one format per prefix → one table per folder).

**Schema-on-read.** Athena stores nothing. The Glue crawler scans `staging/` and writes table definitions — location, schema, and format — into the Glue Data Catalog. At query time Athena reads the catalog, then reads the Parquet files straight from S3. Nothing is ever loaded into a database.

**dbt transformation.**
- **Staging** models mirror each raw source one-to-one, flatten nested fields to snake_case, and standardize types. This layer uses dbt `source()`.
- **Marts** apply business logic. `fct_trials_summary` combines the two trials sources with a `UNION` (they share a schema; no shared key exists for a join) and aggregates trial counts and total enrollment by condition and overall status. This layer uses dbt `ref()`.
- **Tests** (`not_null`, `accepted_values`) run on every build — the automated equivalent of the manual reconciliation checks behind a clinical database lock.

**Orchestration.** The Airflow DAG fetches all three sources in parallel, archives raw, converts and uploads to staging, then **fans in** to a single Glue-crawler trigger once all uploads complete.

---

## dbt lineage

The dbt-generated lineage graph — sources → staging → marts:

<!-- Run `dbt docs generate` then `dbt docs serve --port 8081`, open the lineage graph, screenshot it, save as docs/lineage.png -->
![dbt lineage graph](docs/lineage.png)

---

## Data sources

| Source | API | Notes |
|---|---|---|
| Trials (heart disease) | ClinicalTrials.gov v2 | Nested JSON, flattened in staging |
| Trials (diabetes) | ClinicalTrials.gov v2 | Same schema as above |
| Adverse events | OpenFDA (FAERS) | Currently a **heart-disease-filtered slice**, not all FAERS data |

> Trials and adverse events share **no common key** (`nct_id` vs `safety_report_id`), so they are modeled as **two separate stars** rather than forced into a join.

---

## Running it locally

```bash
# Infrastructure
cd terraform && terraform init && terraform apply

# Ingestion + orchestration (Airflow in Docker)
cd airflow && docker compose up

# dbt (from inside clinical_dbt/, with venv active)
dbt run
dbt test
dbt docs generate && dbt docs serve --port 8081
```

---

## Next steps / roadmap

- **Stateless S3 tasks.** The DAG currently passes *local file paths* between tasks, which assumes a shared filesystem (fine on LocalExecutor, but breaks under distributed executors like Celery/Kubernetes). Refactor to write to and read from S3 directly, passing S3 keys so tasks are stateless and portable.
- **Adverse-events mart.** Build the second star (e.g. counts by country, seriousness rate) — no shared key with trials, so it stands alone.
- **Stronger CI.** Have GitHub Actions run `dbt build` (compile + run + test) on every push, not just a version check.
- **Parameterize the trials fetchers.** Fold the two near-identical ClinicalTrials.gov fetchers into one parameterized fetcher.
- **Rename the adverse-events prefix/table** to reflect that it is a heart-disease-filtered slice.