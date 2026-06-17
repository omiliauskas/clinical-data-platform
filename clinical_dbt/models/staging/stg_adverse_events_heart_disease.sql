SELECT
    safetyreportid AS safety_report_id,
    CASE WHEN serious = 1 THEN 1 ELSE 0 END AS is_serious,
    CASE WHEN seriousnessdeath = 1.0 THEN 1 ELSE 0 END AS is_death,
    CASE WHEN seriousnesshospitalization = 1.0 THEN 1 ELSE 0 END AS is_hospitalization,
    primarysourcecountry AS primary_source_country,
    occurcountry AS occur_country,
    receivedate AS receive_date,
    reporttype AS report_type
FROM {{ source('clinical', 'adverse_events_heart_disease') }}