{{ config(external_location='s3://clinical-data-platform-omiliauskas/marts/fct_trials_summary/') }}

SELECT
    c.condition,
    s.overall_status,
    COUNT(*)                AS trials_count,
    SUM(f.enrollment_count) AS total_enrollment
FROM {{ ref('fct_trials') }} f
JOIN {{ ref('dim_condition') }} c ON f.condition_key = c.condition_key
JOIN {{ ref('dim_status') }}    s ON f.overall_status_key = s.overall_status_key
GROUP BY c.condition, s.overall_status