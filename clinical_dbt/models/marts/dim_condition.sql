{{ config(external_location='s3://clinical-data-platform-omiliauskas/marts/dim_condition/') }}

WITH conditions AS (

    SELECT 'heart_disease' AS condition
    UNION ALL
    SELECT 'diabetes' AS condition

)

SELECT
    {{ dbt_utils.generate_surrogate_key(['condition']) }} AS condition_key,
    condition
FROM conditions