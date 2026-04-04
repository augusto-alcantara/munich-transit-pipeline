import logging
from db import get_connection
from repository import (
    get_transit_departures_count, 
    create_raw_transit_table,
    insert_raw_transit,
    create_transit_table,
    truncate_transit_departures,
    insert_transit_departure
    )
from ingestion import fetch_mvg_data
from transformation import transform_departures
from datetime import datetime


logging.basicConfig(level=logging.INFO)


def main():
    conn = get_connection()
    
    try:
        data = fetch_mvg_data()
        ingested_at = datetime.now()

        create_raw_transit_table(conn)
        create_transit_table(conn)
        # truncate_transit_departures(conn)
        insert_raw_transit(conn, data)

        rows = transform_departures(data, ingested_at)

        for row in rows:
            insert_transit_departure(
                conn,
                row["line"],
                row["destination"],
                row["transport_type"],
                row["planned_departure_time"],
                row["delay_minutes"],
                row["platform"],
                row["ingested_at"]
            )
        
        conn.commit()

    except Exception as e:
        logging.exception("Transaction failed")
        conn.rollback()
        
    finally:
        count = get_transit_departures_count(conn)
        logging.info("Transit departures row count: %s", count)

        conn.close()

if __name__ == "__main__":
    main()


