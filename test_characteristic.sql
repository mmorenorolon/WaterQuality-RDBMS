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
