from datetime import datetime
from src.transformation import transform_departures

def test_transform_departures_skips_rows_missing_required_fields():
    ingested_at = datetime.now()
    
    sample_data = [
        {
            "label": "U2",
            "destination": "Messestadt Ost",
            "transportType": "UBAHN",
            "plannedDepartureTime": 1712500000000,
            "delayInMinutes": 2,
            "platform": "1"
        },
        {
            "label": None,
            "destination": "Hauptbahnhof",
            "transportType": "TRAM",
            "plannedDepartureTime": 1712500000000,
            "delayInMinutes": 0,
            "platform": "2"
        },
        {
            "label": "S1",
            "destination": None,
            "transportType": "SBAHN",
            "plannedDepartureTime": 1712500000000,
            "delayInMinutes": 1,
            "platform": "3"
        }
    ]
    
    rows = transform_departures(sample_data, ingested_at)
    
    assert len(rows) == 1
    assert rows[0]["line"] == "U2"
    assert rows[0]["destination"] == "Messestadt Ost"

def test_transform_departures_handles_invalid_timestamp():
    from datetime import datetime

    ingested_at = datetime.now()

    sample_data = [
        {
            "label": "U2",
            "destination": "Messestadt Ost",
            "transportType": "UBAHN",
            "plannedDepartureTime": "invalid_timestamp",
            "delayInMinutes": 2,
            "platform": "1"
        }
    ]

    rows = transform_departures(sample_data, ingested_at)

    assert len(rows) == 1
    assert rows[0]["planned_departure_time"] is None
