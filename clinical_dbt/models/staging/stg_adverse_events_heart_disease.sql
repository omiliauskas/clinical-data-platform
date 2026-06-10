SELECT
    safetyreportid AS safety_report_id,
    serious AS is_serious,
    seriousnessdeath AS is_death,
    seriousnesshospitalization AS is_hospitalization,
    primarysourcecountry AS primary_source_country,
    occurcountry AS occur_country,
    receivedate AS receive_date,
    reporttype AS report_type
FROM {{ source('clinical', 'adverse_events_heart_disease') }}