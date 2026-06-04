CREATE TABLE result (
    result_pk INTEGER PRIMARY KEY,
    activity_pk INTEGER NOT NULL,
    characteristic_id INTEGER NOT NULL,

    activity_id_source TEXT,
    station_id_source TEXT,

    result_value DOUBLE,
    result_unit TEXT,

    result_detection_condition TEXT,
    result_status TEXT,
    result_sample_fraction TEXT,
    measure_qualifier TEXT,

    detection_limit_value DOUBLE,
    detection_limit_unit TEXT,
    detection_limit_type TEXT,

    analytical_method_id TEXT,
    analytical_method_context TEXT,
    analytical_method_name TEXT,

    result_comment TEXT,
    provider_name TEXT,

    FOREIGN KEY (activity_pk)
        REFERENCES activity(activity_pk),

    FOREIGN KEY (characteristic_id)
        REFERENCES characteristic(characteristic_id)
);

COPY result (
    result_pk,
    activity_pk,
    characteristic_id,

    activity_id_source,
    station_id_source,

    result_value,
    result_unit,

    result_detection_condition,
    result_status,
    result_sample_fraction,
    measure_qualifier,

    detection_limit_value,
    detection_limit_unit,
    detection_limit_type,

    analytical_method_id,
    analytical_method_context,
    analytical_method_name,

    result_comment,
    provider_name
)
FROM 'data_processed/result_clean.csv'
DELIMITER ','
CSV HEADER;
