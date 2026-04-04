from datetime import datetime
import logging

def transform_departures(data, ingested_at):
    rows = []
    skipped_rows = 0
    invalid_timestamp = 0
    missing_delay = 0
    missing_platform = 0

    for item in data:
        # Validate required fiels: line, destination
        if not item.get("label") or not item.get("destination"):
            skipped_rows +=1
            continue # Skip this row if essential fields are missing

        # Handle the planned departure time (convert from epoch or set to None)
        raw_time = item.get("plannedDepartureTime")
        if isinstance(raw_time, (int, float)):
            try:
                planned_departure_time = datetime.fromtimestamp(raw_time / 1000)
            except Exception:
                planned_departure_time = None
                invalid_timestamp += 1
        else:
            planned_departure_time = None
            invalid_timestamp += 1

        # Validate delay ( it should be an integer, otherwise None)
        try:
            delay_minutes = int(item.get("delayInMinutes", None))
        except (ValueError, TypeError):
            delay_minutes = None
            missing_delay += 1
        
        # Handle platform (nullable field, allow None if missing)
        platform = item.get("platform", None)
        if not platform:
            missing_platform += 1

        # Build the structured row
        row = {
            "line" : item.get("label"),
            "destination" : item.get("destination"),
            "transport_type" : item.get("transportType"),
            "planned_departure_time" : planned_departure_time,
            "delay_minutes" : delay_minutes,
            "platform" : platform,
            "ingested_at" : ingested_at
        }

        rows.append(row)

    # Log the quality summary
    logging.info(f"Rows processed: {len(data)}")
    logging.info(f"Rows skipped (missing required fields): {skipped_rows}")
    logging.info(f"Rows with missing platform: {missing_platform}")
    logging.info(f"Rows with invalid delays: {missing_delay}")
    logging.info(f"Rows with invalid timestamps: {invalid_timestamp}")

    return rows

