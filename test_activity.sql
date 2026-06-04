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
