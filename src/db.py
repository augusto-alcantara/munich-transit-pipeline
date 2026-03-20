import psycopg2


def get_connection():
    return psycopg2.connect(
        dbname="de_project",
        user="postgres",
        password="15873642901234",
        host="localhost",
        port=5432,
    )