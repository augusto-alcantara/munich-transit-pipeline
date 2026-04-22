import json


def create_raw_transit_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_transit_data (
                id SERIAL PRIMARY KEY,
                extraction_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                raw_json JSONB,
                source_api TEXT
            );
        """)


def insert_raw_transit(conn, json_data):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO raw_transit_data (raw_json, source_api)
            VALUES (%s, %s);
        """,(json.dumps(json_data), "MVG_API"))


def create_transit_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transit_departures(
                id SERIAL PRIMARY KEY,
                line TEXT,
                destination TEXT,
                transport_type TEXT,
                planned_departure_time TIMESTAMP,
                delay_minutes INTEGER,
                platform TEXT,
                ingested_at TIMESTAMP NOT NULL,
                UNIQUE (line, destination, transport_type, planned_departure_time)
            );
        """)


def insert_transit_departure(
    conn, 
    line, 
    destination, 
    transport_type, 
    planned_departure_time, 
    delay_minutes, 
    platform, 
    ingested_at
):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO transit_departures (
                line,
                destination,
                transport_type,
                planned_departure_time,
                delay_minutes,
                platform,
                ingested_at    
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)  
            """,
            (
                line,
                destination,
                transport_type,
                planned_departure_time,
                delay_minutes,
                platform,
                ingested_at
            )
        )


def insert_transit_departures_batch(conn, rows):
    with conn.cursor() as cursor:

        data = [
            (
                row['line'],
                row['destination'],
                row['transport_type'],
                row['planned_departure_time'],
                row['delay_minutes'],
                row['platform'],
                row['ingested_at']
            )
            for row in rows
        ]

        query = """
        INSERT INTO transit_departures (
            line,
            destination,
            transport_type,
            planned_departure_time,
            delay_minutes,
            platform,
            ingested_at
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (line, destination, transport_type, planned_departure_time)
        DO NOTHING
        """

        cursor.executemany(query, data)


def truncate_transit_departures(conn):
    with conn.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE transit_departures;")


def get_transit_departures_count(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM transit_departures;")
        return cursor.fetchone()[0]


def get_raw_transit_data(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT raw_json FROM raw_transit_data ORDER BY id DESC LIMIT 1;")
        result = cursor.fetchone()
        return result[0] if result else []