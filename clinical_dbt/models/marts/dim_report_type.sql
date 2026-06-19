{{ config(external_location='s3://clinical-data-platform-omiliauskas/marts/dim_report_type/') }}

SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['report_type']) }} AS report_type_key,
    report_type
FROM {{ ref('stg_adverse_events_heart_disease') }}