-- Average delay per line
SELECT line,
       AVG(delay_minutes) AS avg_delay
FROM transit_departures
WHERE delay_minutes IS NOT NULL
GROUP BY line
ORDER BY avg_delay DESC;

-- Top lines by frequency
SELECT line, COUNT(*)
FROM transit_departures
GROUP BY line
ORDER BY COUNT(*) DESC;

-- Average delay by hour of day
-- Insight: delays increase in the afternoon and peak around 16–17h, while mornings are more stable.
-- Some negative delays indicate early departures.

SELECT 
    EXTRACT(HOUR FROM planned_departure_time) AS hour,
    ROUND(AVG(delay_minutes), 2) AS avg_delay
FROM transit_departures
WHERE delay_minutes IS NOT NULL
GROUP BY hour
ORDER BY hour;