# Munich Transit Pipeline

A data engineering pipeline that ingests raw data from the MVG API, transforms it into a structured format, applies data quality validation, and loads it into a PostgreSQL database with built-in failure handling and observability.

---

## Overview

This project demonstrates a basic data engineering pipeline design, including ingestion, raw storage, transformation, and analytical modeling using SQL and dbt.
The focus is not just moving data, but designing a small pipeline that is queryable, testable, and more reliable under imperfect real-world input.

---

## Key Features

- Separation of ingestion and transformation tasks
- Idempotent data loading using UNIQUE constraints and conflict handling
- Transaction management with commit / rollback
- Logging for observability and debugging
- Raw + structured data modeling

---

## What it does

- Fetches real-time transit departure data from the MVG API
- Stores raw API responses in PostgreSQL (`JSONB`)
- Transforms raw records into a structured table (`transit_departures`)
- Applies basic data quality rules (required vs nullable fields)
- Preserves historical snapshots across runs using ingestion timestamps
- Logs pipeline stages and failures for better observability
- Aborts safely on suspicious empty ingestion results
- Uses transactions and rollback to avoid partial writes on failure
- Enables analytical queries on transit operations (counts, delays, distribution, snapshot comparison)

---

## Pipeline Architecture

```text
Pipeline execution (Python)

MVG API → ingestion → raw_transit_data (PostgreSQL)
                ↓
         transformation
                ↓
        transit_departures
```

---

## Data Modeling with dbt

A lightweight dbt layer was introduced to separate analytical modeling from ingestion and transformation logic.

While the Python pipeline handles data ingestion, raw storage, and initial structuring, dbt is used to define clean, analytics-ready models directly in SQL.

---

### Updated Architecture

```text
API → Python → PostgreSQL (transit_departures)
                         ↓
                        dbt
                         ↓
              clean_transit_departures
```

---

### Purpose

- separates data processing from analytical modeling
- enables SQL-based transformations for analytics
- improves clarity and maintainability of the data layer

This reflects a more realistic data engineering pattern where ingestion and modeling are handled in distinct layers.

---

## Architecture

The pipeline is executed through a Python entry point (`main.py`) and is divided into two main stages:

- **Ingestion task**
  - Fetches data from the MVG API
  - Stores raw JSON in the `raw_transit_data` table

- **Transformation task**
  - Reads raw data from PostgreSQL
  - Applies transformation and data quality rules
  - Writes structured data into `transit_departures`

Each task is independent and communicates through the database, rather than sharing data in memory.

---

## Failure Handling & Observability

The pipeline classifies failures into retryable, non-retryable, and non-critical. Retryable errors, such as API or network failures, raise exceptions and are treated as retryable and can be retried in a production orchestrator. Non-retryable errors, like failed data validation, stop the pipeline to protect data quality. Non-critical situations, such as empty data, are logged as warnings and handled safely. Structured logs clearly indicate the stage, type of failure, and system behavior, making debugging easier without reading the code.

---

## Engineering Decisions

### Raw vs Structured Storage

The pipeline stores both raw and structured data:

- `raw_transit_data` preserves the original API response for traceability and reprocessing
- `transit_departures` provides a clean analytical model optimized for SQL queries

This separation reflects a common data engineering pattern: ingest first, model later.

---

### Required vs Nullable Fields

- `line` and `destination` are treated as required fields  
  → rows missing these are skipped

- `delay_minutes` and `platform` are nullable  
  → useful but not critical for defining a departure event

This distinction ensures analytical usability without over-discarding data.

---

### Timestamp Handling

The API provides timestamps in epoch milliseconds.

These are converted into PostgreSQL `TIMESTAMP` values during transformation.

Invalid timestamps are safely set to `NULL`.

---

### Event Time vs Ingestion Time

The pipeline stores two different time concepts:

- `planned_departure_time` → when the transit event is supposed to happen
- `ingested_at` → when the pipeline retrieved and stored the data

This distinction makes the model more realistic and allows the pipeline to preserve historical observations across runs.

---

### Historical Snapshot Design

The structured table now uses **append-based loading** instead of being rebuilt on each run.

Each pipeline execution generates one ingestion timestamp (`ingested_at`) shared across all rows inserted in that run.

This allows the project to preserve **historical snapshots** over time instead of only storing the latest observed state.

This reflects a more realistic batch-processing pattern where each run represents one observation moment.

---

## Reliability & Testing

The pipeline includes a first reliability layer focused on controlled failure behavior, data quality handling, and observability.

### Reliability improvements
- clearer logging across pipeline stages
- safer handling of API/network failures
- safe abort behavior when ingestion returns an ambiguous empty result
- transaction rollback on failure to prevent partial writes

### Controlled failure validation
The pipeline was manually tested under failure scenarios such as:
- broken database connection
- forced insert failure (`NOT NULL` constraint violation)

These checks were used to verify that failures are visible, understandable, and do not leave the database in an inconsistent state.

### Automated tests
A focused `pytest` test layer was added for `transformation.py`, covering key transformation and data-quality behaviors such as:

- valid row transformation
- skipping rows missing required fields
- invalid timestamp handling
- invalid delay fallback to `NULL`
- missing optional platform handling

Run tests with:

```bash
python -m pytest -v
```

---

## Tech stack

- Python
- PostgreSQL
- psycopg2
- requests
- DBeaver / psql for database inspection

---

## Project structure

```text
src/
├── db.py
├── ingestion.py
├── main.py
├── repository.py
├── check_connection.py
├── transformation.py

tests/
├── test_transformation.py
```

- **main.py** — orchestrates the pipeline execution  
- **ingestion.py** — fetches data from the MVG API  
- **transformation.py** — applies transformation and data quality logic  
- **repository.py** — contains SQL queries and database operations  
- **db.py** — manages database connections  
- **check_connection.py** — simple script to manually verify API connectivity

- **tests/test_transformation.py** — automated tests for transformation logic and data quality handling
---

## Database tables

### `raw_transit_data`

Stores the original API response as raw JSON.

### `transit_departures`

Stores structured departure rows with:

- `line`
- `destination`
- `transport_type`
- `planned_departure_time`
- `delay_minutes`
- `platform`
- `ingested_at`

---

## Example SQL queries

```sql
SELECT * FROM transit_departures;
```

```sql
SELECT line, COUNT(*)
FROM transit_departures
GROUP BY line;
```

```sql
SELECT transport_type, COUNT(*)
FROM transit_departures
GROUP BY transport_type;
```

```sql
SELECT line, AVG(delay_minutes)
FROM transit_departures
GROUP BY line;
```

---

## Analytical Use Cases

The structured dataset enables basic operational and analytical insights:

### System reliability (KPI)
- Percentage of delayed departures  
→ measures overall system performance and reliability

### High-delay detection
- Identify departures with delay > 5 minutes  
→ helps detect specific problematic events

### Data quality monitoring
- NULL vs NOT NULL delay analysis  
→ evaluates completeness and reliability of the dataset

### Time-based analysis
- Average delay per hour of day  
→ identifies patterns in delays (e.g. peak hours vs low traffic periods)

These analyses demonstrate how the pipeline output can be used for monitoring, reporting, and operational decision-making.

---

## Data Quality Rules

The transformation layer enforces the following rules:

- Rows missing `line` or `destination` are skipped (required fields)

- `planned_departure_time` is converted from epoch milliseconds to a SQL timestamp  
  → invalid values are stored as `NULL`

- `delay_minutes` and `platform` are nullable  
  → missing values are preserved as `NULL`

- Invalid or missing values in required fields are logged and skipped, ensuring that data issues are visible rather than silently ignored

### Validation

The resulting dataset was validated using SQL queries to confirm:

- required fields are enforced
- incomplete fields remain visible
- the dataset supports basic analytical queries

---

## How to Run

### Requirements

- Python 3.x
- PostgreSQL running locally
- `.env` file with database credentials

---

### Run locally

```bash
python src/main.py
```

### Run tests

```bash
python -m pytest -v
```

### Manually check API connectivity

```bash
python src/check_connection.py
```

---

### Run with Docker

```bash
docker build -t munich-transit-pipeline .
docker run --env-file .env munich-transit-pipeline
```

---

## Learning goals

This project is being built as part of a data engineering learning roadmap focused on:

- Python + SQL fundamentals
- Data ingestion
- Raw vs structured storage
- Transformation logic
- Queryable data models

---

## Status

Actively under development, with current focus on reliability, observability, testing, and historical tracking.

---

## Limitations & Trade-offs

- The pipeline currently processes only a small number of rows, which may hide issues that would appear with larger and more realistic datasets.

- The pipeline currently creates tables during execution, which mixes setup with data processing. These concerns should be separated, with the pipeline focusing only on processing data.

- The pipeline uses local logging, which is not centralized. This limits visibility, as logs are only available on the local machine and cannot be easily accessed or monitored by other systems.

- The pipeline does not include alerting or monitoring, so failures must be checked manually instead of being automatically detected.

---


## Future Improvements

- Introduce a workflow orchestrator (e.g., Airflow) for scheduling, retries, and monitoring
- Deploy pipeline to cloud environment (AWS)
- Expand automated test coverage beyond transformation logic
- Handle schema evolution if API changes