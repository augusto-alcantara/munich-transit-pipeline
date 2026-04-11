
# Data Engineering Learning Log

Chronological record of backend and data engineering skills built during the 6-month Pre-0 phase.

---

## Timeline

- [2026-03-01 — Day 1 — Backend Foundations](#-2026-03-01--day-1--backend-foundations)
- [2026-03-02 — Day 2 — SQL Queries & Repository Architecture](#-2026-03-02--day-2--sql-queries--repository-architecture)
- [2026-03-03 — Day 3 — Transactions, Integrity & Backend Robustness](#-2026--03-03--day-3--transactions-integrity--backend-robustness)
- [2026-03-04 — Day 4 — Analytical SQL & Data Querying](#-2026-03-04--day-4--analytical-sql--data-querying)
- [2026-03-05 — Day 5 — SQL Transformation](#-2026-03-05--day-5--sql-transformation)
- [2026-03-06 - Day 6 — API Ingestion & First Pipeline](#-2026-03-06---day-6--api-ingestion--first-pipeline)
- [2026-03-21 - Day 7 — JSON Querying](#-2026-03-21---day-7--json-querying)
- [2026-03-22 - Day 8 — JSON Expansion](#-2026-03-22---day-8--json-expansion)
- [2026-03-25 — Day 9 — First JSON Transformation](#-2026-03-25--day-9--first-json-transformation)
- [2026-03-26 — Day 10 — Data Model Refinement & First Transit Analytics](#-2026-03-26--day-10--data-model-refinement--first-transit-analytics)
- [2026-03-28 - Day 11 — Pipeline Cleanup & Modular Transformation](#-2026-03-28---day-11--pipeline-cleanup--modular-transformation)
- [2026-04-01 — Day 12 — Data Quality & Analytical Validation](#-2026-04-01--day-12--data-quality--analytical-validation)
- [2026-04-02 — Day 13 — Dockerizing Project 0](#-2026-04-02--day-13--dockerizing-project-0)
- [2026-04-03 — Day 14 — Project Packaging & Explainability](#-2026-04-03--day-14--project-packaging--explainability)
- [2026-04-04 — Day 15 — Historical Tracking Layer](#-2026-04-04--day-15--historical-tracking-layer)
-[2026-04-08 — Day 16 — Pipeline Reliability & Controlled Failure](#-2026-04-08--day-16--pipeline-reliability--controlled-failure)
-[2026-04-09 — Day 17 — Transformation Testing & Behavioral Validation](#-2026-04-09--day-17--transformation-testing--behavioral-validation)
-[2026-04-10 — Day 18 — Snapshot Validation & Data Representativeness](#-2026-04-10--day-18--snapshot-validation--data-representativeness)

---

## 📅 2026-03-01 - Day 1 — Backend Foundations

**What I completed**
* Set up local backend environment connecting Python to PostgreSQL.
* Installed PostgreSQL, created database `de_project`, practiced CLI commands (`\l`, `\d`, `\q`).
* Created Python project with virtual environment and installed `psycopg2-binary`, `requests`, `pytest`.
* Built project structure (`src/`, `tests/`) and understood role of `__init__.py`.
* Connected Python to PostgreSQL, created `users` table, inserted data using parameterized queries (`%s`), queried with `SELECT` + `fetchall()`.
* Debugged environment issues (venv not activated, table missing, wrong package name).

**Insight:** backend applications interact with databases through drivers and TCP connections.


## 📅 2026-03-02 — Day 2 — SQL Queries & Repository Architecture

**What I completed**
* Practiced core SQL query patterns: `INNER JOIN`, `LEFT JOIN`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`, `COALESCE`.
* Learned SQL aggregation concepts, including alias limitations and ordering aggregated results.
* Shifted thinking from individual rows to **datasets and relationships between tables**.
* Implemented layered backend structure:
  - `db.py` → database connection
  - `repository.py` → SQL queries
  - `main.py` → application orchestration
* Debugged environment and Python issues (imports, module resolution, virtual environment activation, typos).
* Learned system design principles: avoid opening DB connections per function, importance of indexes for joins, risks of `fetchall()` at scale, and value of separation of concerns.

**Insight:** backend systems remain manageable when responsibilities are separated into clear layers (connection, queries, orchestration).


## 📅 2026-03-03 — Day 3 — Transactions, Integrity & Backend Robustness

**What I completed**
* Extended data model by adding `orders` table with foreign key to `users` (`ON DELETE CASCADE`) to enforce relational integrity.
* Expanded repository layer with `create_orders_table()` and `insert_order()` while keeping SQL isolated in `repository.py`.
* Tested foreign key violation and observed PostgreSQL enforcing integrity automatically (`ForeignKeyViolation`).
* Learned that transaction failures put the connection into an aborted state until `ROLLBACK`.
* Refactored transaction control: removed `commit()` from repository layer and handled transactions in `main.py` using `try / except / rollback`.
* Implemented proper error handling and structured logging (`logging.info`, `logging.error`, `logging.exception`).
* Added index on `orders(user_id)` and learned indexing trade-offs (faster reads vs slower writes).
* Mental shift: backend code must anticipate failure and preserve data consistency.

**Insight:** reliable backend systems depend on controlled transactions — operations must succeed together or be rolled back to maintain database consistency.


## 📅 2026-03-04 — Day 4 — Analytical SQL & Data Querying

**What I completed**
* Practiced SQL filtering (`WHERE`) and aggregation (`SUM`, `COUNT`, `GROUP BY`).
* Built relational queries using `JOIN` between `users` and `orders`.
* Answered dataset-level questions such as total spent per user and highest spending user.
* Added analytical query functions to `repository.py` and inspected results using logging.
* Read Chapter 1 of *Fundamentals of Data Engineering* and created Anki cards.

**Insight:** SQL transforms relational data into business metrics through aggregation and joins.


## 📅 2026-03-05 — Day 5 — SQL Transformation

**What I completed**
* Explored dataset structure using `COUNT` and `GROUP BY`.
* Practiced aggregation queries (`SUM`, `AVG`, `COUNT`, `GROUP BY`).
* Learned `HAVING` for filtering aggregated results.
* Built analytical queries (user ranking, total revenue).
* Extended `repository.py` with analytics functions.
* Tested queries via `main.py` using logging.
* Read Chapter 2 of *Fundamentals of Data Engineering* (ingestion, transformation, serving concepts).

**Insight:** SQL transforms datasets into aggregated insights that answer business questions.


## 📅 2026-03-06 - Day 6 — API Ingestion & First Pipeline

**What I completed**
* Connected to MVG API using `requests.get()` with parameters and timeout
* Built `fetch_mvg_data()` returning structured data (list of dictionaries)
* Explored API JSON and identified key fields (`label`, `destination`, `transportType`) and inconsistencies
* Created `raw_transit_data` table using PostgreSQL JSONB
* Implemented `insert_raw_transit()` with parameterized queries and `json.dumps()`
* Integrated ingestion in `main.py` (API → Python → PostgreSQL)
* Validated pipeline using `jsonb_pretty`

**Learning:**
* JSON must be serialized (`json.dumps`) before storing in PostgreSQL
* Real-world data is inconsistent → requires flexible raw storage (JSONB)

**Insight:**
Real data engineering starts by capturing raw reality before applying structure.


## 📅 2026-03-21 - Day 7 — JSON Querying

**What I completed**
* Explored JSON structure in PostgreSQL (list of objects)
* Used -> to access JSON and ->> to extract values
* Extracted fields: label, destination, transportType

**Learning:**
* -> returns JSON, ->> returns TEXT
* JSON = list of objects (key → value)

**Insight:**
I am only accessing one element (index 0), so I am sampling, not processing the dataset.


## 📅 2026-03-22 - Day 8 — JSON Expansion

**What I completed**
* Expanded JSON arrays using `jsonb_array_elements()`
* Used alias (`AS train`) to reference each JSON object
* Extracted fields (`label`, `destination`, `transportType`) using `->>`
* Compared `raw_json->0` vs full expansion of all elements

**Learning:**

* `jsonb_array_elements()` turns one array into multiple rows (one per element)
* Each row contains one JSON object and can be accessed using an alias
* `->>` extracts values as text from JSON objects
* Rows are lines in the SQL result, columns define structure

**Insight:**
I moved from sampling a single element to processing the full dataset by expanding JSON into rows.


## 📅 2026-03-25 — Day 9 — First JSON Transformation

**What I completed**
* Designed first structured table from raw transit API data
* Defined correct unit of data: **one row = one departure event**
* Created `transit_departures` with:
  - `line`
  - `destination`
  - `transport_type`
* Built first Python transformation loop:
  - iterated through JSON list
  - extracted fields with `.get()`
  - inserted structured rows into PostgreSQL
* Verified output using:
  - `SELECT * FROM transit_departures`
  - `GROUP BY` queries

**Learning:**
* Raw JSON can be stored in PostgreSQL but is not ideal for direct querying
* Structured tables make querying and analysis simpler
* Pipelines often keep both:
  - raw data for reprocessing
  - structured data for analysis

**Insight:**
* Stored data is not the same as modeled data


## 📅 2026-03-26 — Day 10 — Data Model Refinement & First Transit Analytics

**What I completed**
* Inspected the MVG API response and identified additional operational fields useful for analysis.
* Refined the `transit_departures` schema to include:
  - `planned_departure_time`
  - `delay_minutes`
  - `platform`
* Updated the transformation logic in `main.py` to extract and load the new fields.
* Added rerun safety by truncating `transit_departures` before reloading transformed rows.
* Rebuilt the structured table and verified the transformed output in PostgreSQL.

**Learning**
* Structured tables should prioritize analytical usefulness, not just mirror the raw source.
* Operational fields like planned time, delay, and platform make event data more valuable for analysis.
* Transformation pipelines should be rerunnable and reproducible.

**Insight**
The project is starting to move from raw ingestion toward analytical data modeling.


## 📅 2026-03-28 - Day 11 — Pipeline Cleanup & Modular Transformation

**What I completed**
* Created a new `transformation.py` module and moved transformation logic out of `main.py`
* Refactored `main.py` so it now focuses more cleanly on pipeline orchestration
* Fixed the execution order of the pipeline steps to make table creation and truncation safer
* Improved `get_transit_departures_count()` so it returns a clean numeric value
* Updated the README to reflect the new schema, pipeline flow, and project structure
* Validated that the structured table reload is rerunnable across multiple runs
* Identified that `plannedDepartureTime` was being stored incorrectly as raw epoch milliseconds
* Fixed timestamp transformation so `planned_departure_time` is now stored as a real PostgreSQL timestamp
* Verified the corrected timestamps directly in PostgreSQL

**Learning:**
* Transformation logic should be separated from orchestration to keep the pipeline cleaner and more modular
* A pipeline is not truly correct just because it runs — the data itself must also be stored in the right format
* Source formats and SQL column types need to be explicitly aligned during transformation

**Insight:**
A working pipeline is not enough — clean structure and correct data types matter just as much.


## 📅 2026-04-01 — Day 12 — Data Quality & Analytical Validation

**What I completed**
* Improved `transformation.py` to handle real-world data more safely:
  - skip rows if `line` or `destination` is missing
  - convert valid timestamps from epoch to datetime
  - set invalid timestamps and delays to `None`
  - allow missing `platform` as `None`

* Added data quality tracking (processed rows, skipped rows, missing platform, invalid delays, invalid timestamps)

* Ran analytical SQL queries on `transit_departures` to validate that the structured table is usable:
  - line frequency
  - transport type distribution
  - average delay by line
  - delayed vs on-time categorization
  - platform usage
  - bad row check
  - dataset completeness

* Verified that no rows with missing required fields (`line`, `destination`) enter the structured table

* Identified that some fields (delay, platform) are partially incomplete but still usable for analysis

**Learning:**
* Data pipelines should not only load data but also enforce data quality rules
* Required and nullable fields must be handled differently depending on their importance
* SQL can be used to validate both analytical usefulness and data completeness

**Insight:**
A working pipeline is not necessarily a trustworthy pipeline — data quality and validation are part of the engineering work


## 📅 2026-04-02 — Day 13 — Dockerizing Project 0

**What I completed**
* Added a reproducibility layer to Project 0 by containerizing the pipeline with Docker
* Created `requirements.txt` to declare the Python dependencies required by the project
* Refactored `db.py` to load PostgreSQL connection settings from environment variables using `.env`
* Created a basic `Dockerfile` to package the pipeline into a runnable container
* Built the Docker image and successfully executed the full pipeline inside the container
* Adapted the PostgreSQL connection so the container could connect to the local database using `host.docker.internal`

**Learning:**
* A working project is not necessarily reproducible unless its environment is explicitly defined
* Dependency declaration, configuration management, and execution environment are separate layers of a system
* Containerization requires awareness of runtime differences such as filesystem paths and host networking

**Insight:**
The project now carries not only its logic, but also the environment required to run it more reliably outside the original machine setup.


## 📅 2026-04-03 — Day 14 — Project Packaging & Explainability

**What I completed**
* Rewrote the project README to make the pipeline clear, structured, and portfolio-ready
* Documented the pipeline architecture, project structure, data model, and run instructions
* Added an **Engineering Decisions** section explaining key design choices:
  - raw vs structured storage
  - required vs nullable fields
  - timestamp handling
  - rerunnable pipeline design
* Clarified the role of each module (`main.py`, `db.py`, `repository.py`, `ingestion.py`, `transformation.py`)
* Cleaned the repository for clarity:
  - improved `.gitignore`
  - refactored `test_connection.py` into a clean API validation script

**Learning:**
* A project is not complete just because it works — it must also be understandable, runnable, and explainable
* Engineering decisions (why) are different from data quality rules (what the pipeline enforces)
* Raw and structured data serve different purposes: traceability vs analytical usability
* Reproducibility is part of making a project usable outside the original environment

**Insight:**
A project is not portfolio-ready until another person can understand what it does, how it works, and why it was designed that way.


## 📅 2026-04-04 — Day 15 — Historical Tracking Layer

**What I completed**
* Added historical tracking to the structured `transit_departures` table by introducing a new required field: `ingested_at`
* Updated the transformation logic so each transformed row now includes the ingestion timestamp of the pipeline run
* Updated the insert logic so `ingested_at` is stored together with the structured departure fields
* Changed the structured load behavior from **overwrite** to **append** by disabling table truncation before each run
* Validated that multiple runs now preserve previous records instead of replacing them
* Confirmed that one pipeline run now behaves as one historical snapshot

**Learning**
* Pipelines can be designed with either **overwrite** or **append** behavior depending on whether historical data should be preserved
* There is an important difference between:
  - `planned_departure_time` → when the transit event is supposed to happen
  - `ingested_at` → when the pipeline observed and stored the data
* Historical tracking makes a pipeline more realistic because it allows data to be analyzed across multiple runs instead of only showing the latest state

**Insight**
The pipeline is no longer only loading the current state — it is now starting to behave like a time-aware system that preserves historical observations.


## 📅 2026-04-08 — Day 16 — Pipeline Reliability & Controlled Failure

**What I completed**
* Improved `ingestion.py` so API failures are logged more clearly and handled more safely
* Improved `main.py` logging so the pipeline is easier to observe stage by stage
* Treated empty ingestion results as suspicious and aborted the pipeline safely
* Simulated failure cases:
  - broken DB connection
  - forced insert failure (`NOT NULL` violation)
* Verified that failed runs trigger rollback and do not leave partial writes
* Added first focused tests for `transformation.py` using controlled sample input:
  - skip rows missing required fields
  - handle invalid timestamps safely

**Learning**
* A pipeline should fail clearly and predictably, not just work when everything goes well
* Tests are most useful when they isolate one behavior and do not depend unnecessarily on live external systems

**Insight**
A more serious pipeline is not defined by more tools, but by more predictable behavior and more controlled ways to verify it.


## 📅 2026-04-09 — Day 17 — Transformation Testing & Behavioral Validation

**What I completed**
* Expanded the test layer for `transformation.py` using `pytest`
* Added tests covering both normal and edge-case behaviors:
  - valid row transformation
  - skipping rows missing required fields
  - invalid timestamp handling (`NULL` fallback)
  - invalid delay handling (`NULL` fallback)
  - missing optional platform handling
* Refined test structure for clarity and consistency (naming, organization, separation from non-test scripts)
* Cleaned project structure by separating:
  - automated tests (`tests/`)
  - manual API check script (`check_connection.py`)

**Learning**
* Tests should validate **behavioral guarantees**, not just code execution
* Good test cases come from:
  - expected behavior (happy path)
  - realistic failure cases (messy or invalid input)
* Not everything should be tested — focus on cases that would matter if broken
* Clear separation between test code and utility scripts improves project structure and readability

**Insight**
The pipeline is no longer only “working” — its transformation behavior is now explicitly defined and verifiable through tests, making it more trustworthy and easier to evolve.


## 📅 2026-04-10 — Day 18 — Snapshot Validation & Data Representativeness

### Work Completed
- Generated and validated historical snapshots using `ingested_at`
- Compared snapshot counts across runs to verify pipeline consistency
- Analyzed dataset distribution across snapshots

### Key Learnings
- Data correctness, completeness, and representativeness are different problems
- Small ingestion windows can produce biased datasets
- Validation must consider how data is collected over time, not just its structure

### Insight
A dataset can be technically correct and complete, yet still misleading if it is not representative of reality.