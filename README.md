# Munich Transit Pipeline

A data engineering project that ingests real-time transit data from the Munich MVG API, stores raw JSON in PostgreSQL, and transforms it into a structured analytical table with basic data quality validation.

---

## Overview

This project demonstrates a basic data engineering pipeline design, including ingestion, raw storage, transformation, and analytical modeling using PostgreSQL.
The focus is not just moving data, but designing a small pipeline that is queryable, testable, and more reliable under imperfect real-world input.

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
MVG API → raw_transit_data (JSONB) → transformation.py → transit_departures
```


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

## Data Quality Rules

The transformation layer enforces the following rules:

- Rows missing `line` or `destination` are skipped (required fields)

- `planned_departure_time` is converted from epoch milliseconds to a SQL timestamp  
  → invalid values are stored as `NULL`

- `delay_minutes` and `platform` are nullable  
  → missing values are preserved as `NULL`

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


## Future Improvements

- Add orchestration (Airflow or Dagster)
- Deploy pipeline to cloud environment (AWS)
- Expand automated test coverage beyond transformation logic
- Handle schema evolution if API changes