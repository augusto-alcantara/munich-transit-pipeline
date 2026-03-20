
# Data Engineering Learning Log

Chronological record of backend and data engineering skills built during the 6-month Pre-0 phase.

---

## Timeline

- [2026-03-01 — Day 1 — Backend Foundations](#2026-03-01--day-1--backend-foundations)
- [2026-03-02 — Day 2 — SQL Queries & Repository Architecture](#2026-03-02--day-2--sql-queries--repository-architecture)
- [2026-03-03 — Day 3 — Transactions, Integrity & Backend Robustness](#2026--03-03--day-3--transactions-integrity--backend-robustness)
- [2026-03-04 — Day 4 — Analytical SQL & Data Querying](#2026-03-04--day-4--analytical-sql--data-querying)
- [2026-03-06 - Day 6 — API Ingestion & First Pipeline](#2026-03-06--day-6--api-ingestion--first-pipeline)
---

## 📅 2026-03-01 - Day 1 — Backend Foundations

* Set up local backend environment connecting Python to PostgreSQL.
* Installed PostgreSQL, created database `de_project`, practiced CLI commands (`\l`, `\d`, `\q`).
* Created Python project with virtual environment and installed `psycopg2-binary`, `requests`, `pytest`.
* Built project structure (`src/`, `tests/`) and understood role of `__init__.py`.
* Connected Python to PostgreSQL, created `users` table, inserted data using parameterized queries (`%s`), queried with `SELECT` + `fetchall()`.
* Debugged environment issues (venv not activated, table missing, wrong package name).

**Insight:** backend applications interact with databases through drivers and TCP connections.


## 📅 2026-03-02 — Day 2 — SQL Queries & Repository Architecture

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

* Practiced SQL filtering (`WHERE`) and aggregation (`SUM`, `COUNT`, `GROUP BY`).
* Built relational queries using `JOIN` between `users` and `orders`.
* Answered dataset-level questions such as total spent per user and highest spending user.
* Added analytical query functions to `repository.py` and inspected results using logging.
* Read Chapter 1 of *Fundamentals of Data Engineering* and created Anki cards.

**Insight:** SQL transforms relational data into business metrics through aggregation and joins.


## 📅 2026-03-05 — Day 5 — SQL Transformation

* Explored dataset structure using `COUNT` and `GROUP BY`.
* Practiced aggregation queries (`SUM`, `AVG`, `COUNT`, `GROUP BY`).
* Learned `HAVING` for filtering aggregated results.
* Built analytical queries (user ranking, total revenue).
* Extended `repository.py` with analytics functions.
* Tested queries via `main.py` using logging.
* Read Chapter 2 of *Fundamentals of Data Engineering* (ingestion, transformation, serving concepts).

**Insight:** SQL transforms datasets into aggregated insights that answer business questions.


## 📅 2026-03-06 - Day 6 — API Ingestion & First Pipeline

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


