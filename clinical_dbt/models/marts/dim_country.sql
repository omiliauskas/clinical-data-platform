{{ config(external_location='s3://clinical-data-platform-omiliauskas/marts/dim_country/') }}

WITH countries AS (

    SELECT primary_source_country AS country FROM {{ ref('stg_adverse_events_heart_disease') }}
    UNION
    SELECT occur_country AS country FROM {{ ref('stg_adverse_events_heart_disease') }}

)

SELECT
    {{ dbt_utils.generate_surrogate_key(['country']) }} AS country_key,
    COALESCE(country, 'UNKNOWN') AS country 
FROM countries