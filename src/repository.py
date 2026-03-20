def create_users_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY Key,
            name TEXT NOT NULL
        );
        """)


def insert_user(conn,name):
    with conn.cursor()as cursor:
        cursor.execute(
            "INSERT INTO users (name) VALUES (%s)",
            (name,)
        )


def get_all_users(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users;")
        return cursor.fetchall()


def create_orders_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                       id SERIAL PRIMARY KEY,
                       user_id INTEGER NOT NULL,
                       amount NUMERIC NOT NULL,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       CONSTRAINT fk_user FOREIGN KEY(user_id)
                            REFERENCES users(id)
                                ON DELETE CASCADE
                        );
        """)


def insert_order(conn, user_id, amount):
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO orders (user_id, amount) VALUES (%s, %s);",
            (user_id, amount)
        )


def create_orders_user_index(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_orders_user_id
                ON orders(user_id);
        """)


def get_orders_by_user(conn, user_id):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM orders WHERE user_id = %s;",
            (user_id,)
        )
        return cursor.fetchall()
    

def get_total_spent_per_user(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT users.name, SUM(orders.amount) AS total_spent
            FROM users
            JOIN orders
            ON users.id = orders.user_id
            GROUP BY users.name;
        """)
        return cursor.fetchall()
    

def get_user_orders_summary(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT users.name,
                SUM(orders.amount) AS total_spent,
                COUNT(orders.id) AS number_of_orders
            FROM users
            JOIN orders
            ON users.id = orders.user_id
            GROUP BY users.name;
        """)
        return cursor.fetchall()
    

def create_orders_user_index(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_orders_user_id
                ON orders(user_id);
        """)


def get_total_revenue(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT SUM(amount) FROM orders;")
        return cursor.fetchone()
    

def get_average_order_value(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT AVG(amount) FROM orders;")
        return cursor.fetchone()
    

def get_order_count_per_user(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT user_id, COUNT(*)
            FROM orders
            GROUP BY user_id
        """)
        return cursor.fetchall()


def get_users_with_multiple_orders(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT user_id, COUNT(*)
            FROM orders
            GROUP BY user_id 
            HAVING COUNT(*) > 1;
        """)
        return cursor.fetchall()
    

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

    
import json

def insert_raw_transit(conn, json_data):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO raw_transit_data (raw_json, source_api)
            VALUES (%s, %s);
        """,(json.dumps(json_data), "MVG_API"))