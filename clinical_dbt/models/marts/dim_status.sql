{{ config(external_location='s3://clinical-data-platform-omiliauskas/marts/dim_status/') }}

WITH trials_status AS (

    SELECT overall_status FROM {{ ref('stg_trials_heart_disease') }}
    UNION
    SELECT overall_status FROM {{ ref('stg_trials_diabetes') }}

)

SELECT
    {{ dbt_utils.generate_surrogate_key(['overall_status']) }} AS overall_status_key,
    overall_status
FROM trials_status