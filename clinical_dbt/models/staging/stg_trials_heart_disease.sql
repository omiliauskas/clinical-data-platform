SELECT 
    protocolsection.identificationModule.nctId as nct_id,
    protocolsection.identificationModule.briefTitle AS brief_title,
    protocolsection.statusModule.overallStatus AS overall_status,
    protocolsection.designModule.enrollmentInfo.count AS enrollment_count,
    protocolsection.designModule.studyType AS study_type

FROM {{ source('clinical', 'trials_heart_disease') }}