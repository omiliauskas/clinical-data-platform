{{ config(external_location='s3://clinical-data-platform-omiliauskas/marts/dim_study_type/') }}

WITH trials_study_type AS (

    SELECT study_type FROM {{ ref('stg_trials_heart_disease') }}
    UNION
    SELECT study_type FROM {{ ref('stg_trials_diabetes') }}

)

SELECT
    {{ dbt_utils.generate_surrogate_key(['study_type']) }} AS study_type_key,
    study_type
FROM trials_study_type