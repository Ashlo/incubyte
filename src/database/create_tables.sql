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
    -- Derived columns
    age INTEGER GENERATED ALWAYS AS (
        CAST(strftime('%Y', 'now') AS INTEGER) - CAST(strftime('%Y', dob) AS INTEGER)
    ),
    days_since_consulted INTEGER GENERATED ALWAYS AS (
        CAST(julianday('now') - julianday(last_consulted_date) AS INTEGER)
    ),
    needs_consultation INTEGER GENERATED ALWAYS AS (
        CASE WHEN (julianday('now') - julianday(last_consulted_date)) > 30 THEN 1 ELSE 0 END
    ),
    PRIMARY KEY (customer_id, country)
);

-- Country-specific tables
CREATE TABLE IF NOT EXISTS table_india AS SELECT * FROM staging_vaccination_records WHERE 1=0;
CREATE TABLE IF NOT EXISTS table_usa AS SELECT * FROM staging_vaccination_records WHERE 1=0;
CREATE TABLE IF NOT EXISTS table_australia AS SELECT * FROM staging_vaccination_records WHERE 1=0; 