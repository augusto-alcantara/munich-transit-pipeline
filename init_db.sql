-- This table serves as the landing zone for the raw data of the Munich API.

CREATE TABLE IF NOT EXISTS raw_transit_data (
    id SERIAL PRIMARY KEY,
    extraction_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_json JSONB NOT NULL,
    source_api TEXT NOT NULL,
    status_code INTEGER
);

-- Index for faster filtering and time-based queries
CREATE INDEX IF NOT EXISTS idx_extraction_ts ON raw_transit_data (extraction_ts);

COMMENT ON TABLE raw_transit_data IS 'Landing table for raw JSON responses from Munich Transit APIs';


