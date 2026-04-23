
# Data Engineering Learning Log

Chronological record of backend and data engineering skills built during the 6-month Pre-0 phase.
Iterations represent learning cycles and system improvements, not calendar days.

---

## Timeline

- [2026-03-01 — Iteration 1 — Backend Foundations](#iteration-1--backend-foundations)
- [2026-03-02 — Iteration 2 — SQL Queries & Repository Architecture](#iteration-2--sql-queries--repository-architecture)
- [2026-03-03 — Iteration 3 — Transactions, Integrity & Backend Robustness](#iteration-3--transactions-integrity--backend-robustness)
- [2026-03-04 — Iteration 4 — Analytical SQL & Data Querying](#iteration-4--analytical-sql--data-querying)
- [2026-03-05 — Iteration 5 — SQL Transformation](#iteration-5--sql-transformation)
- [2026-03-06 — Iteration 6 — API Ingestion & First Pipeline](#iteration-6--api-ingestion--first-pipeline)
- [2026-03-21 — Iteration 7 — JSON Querying](#iteration-7--json-querying)
- [2026-03-22 — Iteration 8 — JSON Expansion](#iteration-8--json-expansion)
- [2026-03-25 — Iteration 9 — First JSON Transformation](#iteration-9--first-json-transformation)
- [2026-03-26 — Iteration 10 — Data Model Refinement & First Transit Analytics](#iteration-10--data-model-refinement--first-transit-analytics)
- [2026-03-28 — Iteration 11 — Pipeline Cleanup & Modular Transformation](#iteration-11--pipeline-cleanup--modular-transformation)
- [2026-04-01 — Iteration 12 — Data Quality & Analytical Validation](#iteration-12--data-quality--analytical-validation)
- [2026-04-02 — Iteration 13 — Dockerizing Project 0](#iteration-13--dockerizing-project-0)
- [2026-04-03 — Iteration 14 — Project Packaging & Explainability](#iteration-14--project-packaging--explainability)
- [2026-04-04 — Iteration 15 — Historical Tracking Layer](#iteration-15--historical-tracking-layer)
- [2026-04-08 — Iteration 16 — Pipeline Reliability & Controlled Failure](#iteration-16--pipeline-reliability--controlled-failure)
- [2026-04-09 — Iteration 17 — Transformation Testing & Behavioral Validation](#iteration-17--transformation-testing--behavioral-validation)
- [2026-04-10 — Iteration 18 — Snapshot Validation & Data Representativeness](#iteration-18--snapshot-validation--data-representativeness)
- [2026-04-11 — Iteration 19 — Observability & SQL Analysis](#iteration-19--observability--sql-analysis)
- [2026-04-13 — Iteration 20 — Analytical Thinking & SQL Patterns](#iteration-20--analytical-thinking--sql-patterns)
- [2026-04-14 — Iteration 21 — Pipeline Consistency & SQL Structuring](#iteration-21--pipeline-consistency--sql-structuring)
- [2026-04-15 — Iteration 22 — Insert Optimization (Scalability)](#iteration-22--insert-optimization-scalability)
- [2026-04-15 — Iteration 23 — Logging & Observability](#iteration-23--logging--observability)
- [2026-04-17/19 — Iteration 24 — Airflow Integration & System Thinking](#iteration-24--airflow-integration--system-thinking)
- [2026-04-20/21 — Iteration 25 — Data Exploration & SQL Understanding](#iteration-25--data-exploration--sql-understanding)
- [2026-04-20/21 — Iteration 26 — Retries & Failure Types](#iteration-26--retries--failure-types)
- [2026-04-20/21 — Iteration 27 — Failure Observation & System Behavior](#iteration-27--failure-observation--system-behavior)
- [2026-04-20/21 — Iteration 28 — Failure Handling & Logging](#iteration-28--failure-handling--logging)

---

## Iteration 1 — Backend Foundations
📅 2026-03-01

**What I completed**
* Set up local backend environment connecting Python to PostgreSQL.
* Installed PostgreSQL, created database `de_project`, practiced CLI commands (`\l`, `\d`, `\q`).
* Created Python project with virtual environment and installed `psycopg2-binary`, `requests`, `pytest`.
* Built project structure (`src/`, `tests/`) and understood role of `__init__.py`.
* Connected Python to PostgreSQL, created `users` table, inserted data using parameterized queries (`%s`), queried with `SELECT` + `fetchall()`.
* Debugged environment issues (venv not activated, table missing, wrong package name).

**Insight:** backend applications interact with databases through drivers and TCP connections.


---

## Iteration 2 — SQL Queries & Repository Architecture
📅 2026-03-02

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


---

## Iteration 3 — Transactions, Integrity & Backend Robustness
📅 2026-03-03

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


---

## Iteration 4 — Analytical SQL & Data Querying
📅 2026-03-04

**What I completed**
* Practiced SQL filtering (`WHERE`) and aggregation (`SUM`, `COUNT`, `GROUP BY`).
* Built relational queries using `JOIN` between `users` and `orders`.
* Answered dataset-level questions such as total spent per user and highest spending user.
* Added analytical query functions to `repository.py` and inspected results using logging.
* Read Chapter 1 of *Fundamentals of Data Engineering* and created Anki cards.

**Insight:** SQL transforms relational data into business metrics through aggregation and joins.


---

## Iteration 5 — SQL Transformation
📅 2026-03-05

**What I completed**
* Explored dataset structure using `COUNT` and `GROUP BY`.
* Practiced aggregation queries (`SUM`, `AVG`, `COUNT`, `GROUP BY`).
* Learned `HAVING` for filtering aggregated results.
* Built analytical queries (user ranking, total revenue).
* Extended `repository.py` with analytics functions.
* Tested queries via `main.py` using logging.
* Read Chapter 2 of *Fundamentals of Data Engineering* (ingestion, transformation, serving concepts).

**Insight:** SQL transforms datasets into aggregated insights that answer business questions.


---

## Iteration 6 — API Ingestion & First Pipeline
📅 2026-03-06

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


---

## Iteration 7 — JSON Querying
📅 2026-03-21

**What I completed**
* Explored JSON structure in PostgreSQL (list of objects)
* Used -> to access JSON and ->> to extract values
* Extracted fields: label, destination, transportType

**Learning:**
* -> returns JSON, ->> returns TEXT
* JSON = list of objects (key → value)

**Insight:**
I am only accessing one element (index 0), so I am sampling, not processing the dataset.


---

## Iteration 8 — JSON Expansion
📅 2026-03-22

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


---

## Iteration 9 — First JSON Transformation
📅 2026-03-25

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


---

## Iteration 10 — Data Model Refinement & First Transit Analytics
📅 2026-03-26

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


---

## Iteration 11 — Pipeline Cleanup & Modular Transformation
📅 2026-03-28

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


---

## Iteration 12 — Data Quality & Analytical Validation
📅 2026-04-01

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


---

## Iteration 13 — Dockerizing Project 0
📅 2026-04-02

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


---

## Iteration 14 — Project Packaging & Explainability
📅 2026-04-03

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


---

## Iteration 15 — Historical Tracking Layer
📅 2026-04-04

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


---

## Iteration 16 — Pipeline Reliability & Controlled Failure
📅 2026-04-08

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


---

## Iteration 17 — Transformation Testing & Behavioral Validation
📅 2026-04-09

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


---

## Iteration 18 — Snapshot Validation & Data Representativeness
📅 2026-04-10

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


---

## Iteration 19 — Observability & SQL Analysis
📅 2026-04-11

### What I did
- Added logging to the pipeline to make failures visible (missing required fields, invalid timestamp, invalid delay)
- Ran SQL queries to analyze the dataset:
  - distribution of lines
  - average delay
  - delayed vs on-time classification
  - missing vs valid delay values
- Used SQL to better understand how `delay_minutes` behaves

### What I learned
- Not all missing data is a problem:
  - required fields → skip row
  - optional fields → allow NULL
- Logging should focus on real issues to avoid noise
- SQL is used to analyze and validate pipeline output
- Aggregations must consider data quality (e.g., excluding NULL values)

### Insight
A data pipeline must decide what data is valid, what can be missing, and what should be discarded.  
The key is distinguishing between:
- data that breaks the system (remove + log)
- data that is incomplete but usable (keep + handle)


---

## Iteration 20 — Analytical Thinking & SQL Patterns
📅 2026-04-13

### What I did
- Wrote analytical SQL queries on `transit_departures`:
  - percentage of delayed departures (KPI)
  - detection of high-delay events (>5 minutes)
  - NULL vs NOT NULL analysis for `delay_minutes`
  - average delay per hour of day
- Practiced structuring queries step by step instead of writing them all at once
- Focused on explaining queries in plain English (no SQL terms)

### What I learned
- SQL is not just querying data, but answering real system questions:
  - “How reliable is the system?” (KPI)
  - “Which events are problematic?” (event-level analysis)
  - “Is the data trustworthy?” (data quality)
  - “When do problems occur?” (time-based analysis)
- `COUNT(*)` vs `COUNT(column)` is critical for understanding NULL behavior
- `CASE WHEN` enables conditional counting and flexible metrics
- Analytical queries require clear thinking before writing SQL

### Insight
The value of SQL is not in the syntax, but in the ability to translate real-world questions into clear, measurable queries.

### Personal Note
Explaining queries clearly is harder than writing them, but it exposes real understanding gaps.


---

## Iteration 21 — Pipeline Consistency & SQL Structuring
📅 2026-04-14

### What I did

- Deep review of pipeline behavior  
- Analyzed transactions (commit / rollback)  
- Practiced explaining system design  
- Learned and applied CTE in SQL  

### What I learned

- Pipelines should be atomic (all-or-nothing)  
- `commit()` defines when data is actually saved  
- `rollback()` prevents inconsistent states  
- Raw and structured data must stay consistent  
- There is a trade-off between consistency and availability  
- CTE is used to structure multi-step queries, but is not always necessary  

### Key insight

- A working pipeline is not enough — understanding failure behavior and data consistency is what makes it reliable  


---

## 🧱 Iteration 22 — Insert Optimization (Scalability)
## 📅 2026-04-15

### What I did
- Identified inefficiency in row-by-row inserts
- Implemented batch insert using `executemany()`
- Refactored `main.py` to remove per-row insert loop
- Fixed structure and indentation issues

### What I learned (CORE)
- Databases are slow per query → reduce number of queries
- One connection ≠ one query
- Batch operations improve scalability
- Working code is not the same as efficient code

### Key insight
> The bottleneck was not the database connection, but the number of queries executed.

### What is still weak
- Logging was not structured or clear enough
- No visibility into performance
- Still small-scale dataset


---

## 🧱 Iteration 23 — Logging & Observability
## 📅 2026-04-15

### What I did
- Added structured logging with stages (`[INGESTION]`, `[TRANSFORMATION]`, `[LOAD]`, `[DB]`)
- Made logs consistent and more informative (e.g., number of rows inserted)
- Added timing to transformation and load steps

### What I learned (CORE)
- Logs are not just messages — they explain system behavior
- Without timing, I cannot detect bottlenecks
- Not everything needs timing — only parts that can scale
- Good logs allow debugging without reading the code

### Key insight
> A working pipeline is not enough — it must be observable and explainable through logs.

### What is still weak
- The pipeline must be run manually; there is no scheduling yet
- Failures are only visible through logs; there is no automatic alerting
- Performance can be seen per run, but not tracked over time


---

## 🧱 Iteration 24 — Airflow Integration & System Thinking
## 📅 2026-04-17 / 2026-04-18 / 2026-04-19

### What I did
- Integrated existing pipeline into Apache Airflow
- Created DAG with ingestion and transformation tasks
- Refactored pipeline to run as independent tasks
- Fixed data flow (moved from in-memory to database-based flow)
- Implemented transaction handling (commit / rollback) inside tasks
- Ensured idempotent behavior using UNIQUE constraint and ON CONFLICT
- Debugged multiple issues (imports, task failures, data flow bugs)

### What I learned (CORE)
- Airflow is an orchestration layer, not execution logic
- Tasks are independent and do not share memory
- Data must be persisted between tasks (database instead of variables)
- A pipeline is a system of state changes, not just function calls
- Transactions are critical to avoid partial writes
- Idempotency ensures safe re-execution of the pipeline

### Key insight
> The biggest shift was moving from passing variables in code to passing data through the database.

### What is still weak
- No retry or alerting configuration in Airflow
- No incremental processing (full batch each run)
- Pipeline runs locally (not deployed)
- Limited validation of transformed data beyond basic rules


---

### 🧱 Iteration 25 — Data Exploration & SQL Understanding

#### What I did
- Ran pipeline and verified execution  
- Explored dataset using SQL (`COUNT`, `AVG`, `GROUP BY`)  
- Analyzed data distribution (lines, delays, snapshots)  
- Added `valid_ratio` metric to transformation  

#### What I learned (CORE)
- SQL aggregation (`GROUP BY`, `COUNT`, `AVG`) is essential to understand datasets  
- Data from pipelines is often incomplete and biased (sampling)  
- Not all raw data is usable → transformation filters invalid rows  
- `AVG()` ignores `NULL` values → results can be misleading  
- Each pipeline run represents a snapshot, not full reality  

#### Key insight
> The pipeline does not represent reality — it represents sampled snapshots filtered by data quality rules.

#### What is still weak
- Cannot distinguish missing vs real “no delay”  
- No thresholds to evaluate data quality  
- No alerts or validation rules  


---

### 🧱 Iteration 26 — Retries & Failure Types

#### What I did
- Added retries to Airflow DAG  
- Simulated API failure  
- Observed retry behavior in Airflow UI  

#### What I learned (CORE)
- Systems must handle temporary failures  
- Not all failures are equal:  
  - transient → retry works  
  - permanent → retry fails  
- Airflow can automatically retry tasks  
- Retries improve system resilience  

#### Key insight
> A robust pipeline is not one that never fails, but one that can recover from temporary failures automatically.

#### What is still weak
- No alerting (failures are not visible outside logs)  
- No retry strategy tuning  
- No differentiation between error types  


---

### 🧱 Iteration 27 — Failure Observation & System Behavior

#### What I did
- Simulated different failure scenarios:  
  - API failure  
  - empty data  
  - database failure  
- Observed how the pipeline behaves in each case  

#### What I learned (CORE)
- Not all failures are equal  
- Some failures are handled safely, others crash the system  
- Observing failure reveals gaps in system design  

#### Key insight
> A system is not defined by whether it fails, but by how it handles failure.

#### What is still weak
- Some failures still cause uncontrolled behavior  
- Lack of explicit failure handling logic  


---

### 🧱 Iteration 28 — Failure Handling & Logging

#### What I did
- Fixed DB connection handling to avoid crashes  
- Differentiated API failure (`None`) vs empty data (`[]`)  
- Improved logging to clearly explain pipeline behavior  
- Tested failure scenarios and verified system behavior  

#### What I learned (CORE)
- A system should not crash randomly — it must stop intentionally  
- Not all “no data” is the same (failure vs valid empty)  
- Logs are essential to understand what the system is doing  
- Handling failure explicitly makes the pipeline predictable  

#### Key insight
> A system is not reliable because it works, but because it behaves correctly when things go wrong.

#### What is still weak
- No data validation rules enforced yet  
- No thresholds to reject bad data  
- No alerting or monitoring system 