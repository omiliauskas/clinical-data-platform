{{ config(external_location='s3://clinical-data-platform-omiliauskas/marts/dim_date/') }}

WITH dates AS (
    SELECT DISTINCT
        receive_date, 
        date_parse(CAST(receive_date AS VARCHAR), '%Y%m%d') AS full_date 
    FROM {{ ref('stg_adverse_events_heart_disease') }}
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['receive_date']) }} AS date_key,
    full_date,
    EXTRACT(YEAR FROM full_date) AS year,
    EXTRACT(MONTH FROM full_date) AS month,
    EXTRACT(QUARTER FROM full_date) AS quarter,
    EXTRACT(DAY FROM full_date) AS day,
    EXTRACT(DAY_OF_WEEK FROM full_date) AS day_of_week
FROM dates