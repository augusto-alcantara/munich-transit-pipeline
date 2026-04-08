import logging
from db import get_connection
from repository import (
    get_transit_departures_count,
    create_raw_transit_table,
    insert_raw_transit,
    create_transit_table,
    # truncate_transit_departures,
    insert_transit_departure,
)
from ingestion import fetch_mvg_data
from transformation import transform_departures
from datetime import datetime


logging.basicConfig(level=logging.INFO)


def main():
    logging.info("Pipeline started")

    conn = None
    try:
        logging.info("Establishing database connection...")
        conn = get_connection()
        logging.info("Database connection established")

        logging.info("Fetching data from MVG API...")
        data = fetch_mvg_data()
        logging.info("Fetched %d raw records", len(data))
        ingested_at = datetime.now()

        if not data:
            logging.warning(
                "No data returned from ingestion. Aborting pipeline safely."
            )
            return

        logging.info("Preparing database tables...")
        create_raw_transit_table(conn)
        create_transit_table(conn)
        # truncate_transit_departures(conn)

        logging.info("Inserting raw data...")
        insert_raw_transit(conn, data)
        logging.info("Raw data inserted successfully.")

        logging.info("Transforming data...")
        rows = transform_departures(data, ingested_at)
        logging.info("Transformed %d rows", len(rows))

        logging.info("Inserting transformed data...")
        for row in rows:
            insert_transit_departure(
                conn,
                row["line"],
                row["destination"],
                row["transport_type"],
                row["planned_departure_time"],
                row["delay_minutes"],
                row["platform"],
                row["ingested_at"],
            )

        logging.info("Finished inserting transformed rows.")

        logging.info("Committing transaction...")
        conn.commit()
        logging.info("Transaction committed successfully.")

    except Exception:
        logging.exception("Pipeline execution failed")
        if conn:
            conn.rollback()
            logging.info("Transaction rolled back successfully.")

    finally:
        try:
            if conn:    
                count = get_transit_departures_count(conn)
                logging.info("Transit departures row count: %s", count)
        except Exception:
            logging.exception("Failed to retrieve transit departures count")

        try:
            if conn:
                conn.close()
                logging.info("Database connection closed successfully.")
        except Exception:
            logging.exception("Failed to close database connection")


if __name__ == "__main__":
    main()
