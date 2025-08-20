import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv
import os

load_dotenv()


def db_connect():
    def get_connection():
        try:
            parsed_url = urlparse(os.getenv("PSQL_URL"))
            username = parsed_url.username
            password = parsed_url.password
            database = parsed_url.path[1:]
            hostname = parsed_url.hostname
            port = parsed_url.port
            return psycopg2.connect(
                database=database,
                user=username,
                password=password,
                host=hostname,
                port=port,
            )
        except:
            return False

    conn = get_connection()
    if conn:
        print("Connection to the PostgreSQL established successfully.")
    else:
        print("Connection to the PostgreSQL encountered an error.")
