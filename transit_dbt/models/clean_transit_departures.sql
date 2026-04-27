SELECT 
    line,
    destination,
    transport_type,
    planned_departure_time,
    delay_minutes,
    platform,
    ingested_at
FROM transit_departures
WHERE line IS NOT NULL


