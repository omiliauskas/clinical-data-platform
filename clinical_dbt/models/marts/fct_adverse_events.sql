{{ config(
materialized='incremental',
table_type='iceberg',
incremental_strategy='merge',
unique_key='safety_report_id',
format='parquet'
) }}

SELECT
    safety_report_id,
    is_serious,
    is_death,
    is_hospitalization, 
    {{ dbt_utils.generate_surrogate_key(['primary_source_country']) }} AS primary_source_country_key,
    {{ dbt_utils.generate_surrogate_key(['occur_country']) }} AS occur_country_key,
    {{ dbt_utils.generate_surrogate_key(['receive_date']) }} AS date_key,
    {{ dbt_utils.generate_surrogate_key(['report_type']) }} AS report_type_key
FROM {{ ref('stg_adverse_events_heart_disease') }}
