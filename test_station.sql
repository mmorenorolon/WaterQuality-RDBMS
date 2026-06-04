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
