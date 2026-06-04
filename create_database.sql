DROP TABLE IF EXISTS result;
DROP TABLE IF EXISTS characteristic;
DROP TABLE IF EXISTS activity;
DROP TABLE IF EXISTS station;

CREATE TABLE station (
    station_id TEXT PRIMARY KEY,
    station_name TEXT,
    station_type TEXT,
    latitude DOUBLE,
    longitude DOUBLE,
    huc8 TEXT,
    state_code TEXT,
    county_code TEXT,
    provider_name TEXT
);

COPY station (
    station_id,
    station_name,
    station_type,
    latitude,
    longitude,
    huc8,
    state_code,
    county_code,
    provider_name
)
FROM 'data_processed/station_clean.csv'
DELIMITER ','
CSV HEADER;
CREATE TABLE activity (
    activity_pk INTEGER PRIMARY KEY,
    activity_id TEXT NOT NULL,
    station_id TEXT NOT NULL,

    activity_type TEXT,
    activity_start_date DATE,
    activity_start_time TIME,
    activity_media TEXT,

    activity_depth_m DOUBLE,
    activity_depth_original_value DOUBLE,
    activity_depth_original_unit TEXT,
    activity_depth_reference_point TEXT,
    activity_depth_flag TEXT,

    activity_comment TEXT,

    FOREIGN KEY (station_id)
        REFERENCES station(station_id),

    UNIQUE (
        activity_id,
        station_id,
        activity_start_date,
        activity_start_time,
        activity_type,
        activity_media
    )
);

COPY activity (
    activity_pk,
    activity_id,
    station_id,

    activity_type,
    activity_start_date,
    activity_start_time,
    activity_media,

    activity_depth_m,
    activity_depth_original_value,
    activity_depth_original_unit,
    activity_depth_reference_point,
    activity_depth_flag,

    activity_comment
)
FROM 'data_processed/activity_clean.csv'
DELIMITER ','
CSV HEADER;
CREATE TABLE characteristic (
    characteristic_id INTEGER PRIMARY KEY,
    characteristic_name TEXT NOT NULL,
    usgs_pcode TEXT NOT NULL,

    UNIQUE (
        characteristic_name,
        usgs_pcode
    )
);

COPY characteristic (
    characteristic_id,
    characteristic_name,
    usgs_pcode
)
FROM 'data_processed/characteristic_clean.csv'
DELIMITER ','
CSV HEADER;
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
