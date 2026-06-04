WITH trials AS (

    SELECT nct_id, overall_status, enrollment_count, 'heart_disease' AS condition
    FROM {{ ref('stg_trials_heart_disease') }}

    UNION ALL

    SELECT nct_id, overall_status, enrollment_count, 'diabetes' AS condition
    FROM {{ ref('stg_trials_diabetes') }}

)

SELECT
    condition,
    overall_status,
    COUNT(*)              AS trials_count,
    SUM(enrollment_count) AS total_enrollment
FROM trials
GROUP BY condition, overall_status