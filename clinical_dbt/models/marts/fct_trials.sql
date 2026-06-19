{{ config(external_location='s3://clinical-data-platform-omiliauskas/marts/fct_trials/') }}

WITH trials AS (

    SELECT nct_id, enrollment_count, 'heart_disease' AS condition, overall_status, study_type
    FROM {{ ref('stg_trials_heart_disease') }}

    UNION ALL

    SELECT nct_id, enrollment_count, 'diabetes' AS condition, overall_status, study_type
    FROM {{ ref('stg_trials_diabetes') }}

)

SELECT
    nct_id,
    enrollment_count,
    {{ dbt_utils.generate_surrogate_key(['condition']) }} AS condition_key,
    {{ dbt_utils.generate_surrogate_key(['overall_status']) }} AS overall_status_key,
    {{ dbt_utils.generate_surrogate_key(['study_type']) }} AS study_type_key
FROM trials
