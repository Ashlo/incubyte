-- Staging table for initial data load
CREATE TABLE IF NOT EXISTS staging_vaccination_records (
    customer_id VARCHAR(18) NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    open_date DATE NOT NULL,
    last_consulted_date DATE,
    vaccination_id CHAR(5),
    dr_name VARCHAR(255),
    state CHAR(5),
    country CHAR(5),
    dob DATE,
    is_active CHAR(1) DEFAULT 'A',
    age INTEGER,
    days_since_last_consulted INTEGER,
    needs_consultation INTEGER,
    PRIMARY KEY (customer_id, country)
);

-- Country-specific tables (using the same structure)
CREATE TABLE IF NOT EXISTS table_ind AS SELECT * FROM staging_vaccination_records WHERE 1=0;
CREATE TABLE IF NOT EXISTS table_usa AS SELECT * FROM staging_vaccination_records WHERE 1=0;
CREATE TABLE IF NOT EXISTS table_aus AS SELECT * FROM staging_vaccination_records WHERE 1=0; 