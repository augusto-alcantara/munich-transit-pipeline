import logging
from db import get_connection
from repository import (
    get_transit_departures_count,
    create_raw_transit_table,
    insert_raw_transit,
    create_transit_table,
    # truncate_transit_departures,
    insert_transit_departures_batch,
)
from ingestion import fetch_mvg_data
from transformation import transform_departures
from datetime import datetime
import time


logging.basicConfig(level=logging.INFO)


def main():
    logging.info("[PIPELINE] Pipeline started")

    conn = None

    logging.info("[DB] Establishing database connection...")
    try:
        conn = get_connection()
        logging.info("[DB] Database connection established")
    except Exception as e:
        logging.error("[DB] Connection failed: %s", e)
        return

    try:
        logging.info("[INGESTION] Fetching data from MVG API...")
        data = fetch_mvg_data()
        
        if data is None:
            logging.error("[INGESTION] API failure detected. Aborting pipeline.")
            return
        
        if not data:
            logging.warning("[INGESTION] No data returned from API. Pipeline will stop (no rows to process).")
            return
        
        logging.info("[INGESTION] Fetched %d raw records", len(data))

        ingested_at = datetime.now()

        logging.info("[DB] Preparing database tables...")
        create_raw_transit_table(conn)
        create_transit_table(conn)
        # truncate_transit_departures(conn)

        logging.info("[LOAD-RAW] Inserting raw data...")
        insert_raw_transit(conn, data)
        logging.info("[LOAD-RAW] Raw data inserted successfully.")

        logging.info("[TRANSFORMATION] Starting transformation...")
        start = time.time()

        rows = transform_departures(data, ingested_at)

        valid_ratio = len(rows) / len(data) 

        logging.info("[QUALITY] Valid rows ratio: %.2f", valid_ratio)

        if valid_ratio < 0.5:
            logging.warning("[QUALITY] Low valid data ratio detected (%.2f). Data may be unreliable.", valid_ratio)

        end = time.time()
        logging.info("[TRANSFORMATION] Transformed %d rows in %.2f seconds", len(rows), end - start)

        logging.info("[LOAD] Inserting transformed data...")
        start = time.time()

        insert_transit_departures_batch(conn, rows)

        end = time.time()
        logging.info("[LOAD] Inserted %d rows in %.2f seconds", len(rows), end - start)

        logging.info("[DB] Committing transaction...")
        conn.commit()
        logging.info("[DB] Transaction committed successfully.")

    except Exception:
        logging.exception(
            "[PIPELINE] Unexpected failure during execution. "
            "Rolling back transaction"
        )
        if conn:
            conn.rollback()
            logging.info("[DB] Transaction rolled back due to failure.")

    finally:
        try:
            if conn:    
                count = get_transit_departures_count(conn)
                logging.info("[DB] Pipeline completed. Total rows in transit_departures: %s", count)
        except Exception:
            logging.exception("[DB] Failed to retrieve transit departures count")

        try:
            if conn:
                conn.close()
                logging.info("[DB] Database connection closed successfully.")
        except Exception:
            logging.exception("[DB] Failed to close database connection")


if __name__ == "__main__":
    main()
