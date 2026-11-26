import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL was not found in the .env file")

def get_sql_connection():
    return psycopg.connect(DATABASE_URL, sslmode="require")

if __name__ == "__main__":
    with get_sql_connection() as conn:
        print("Connected to database successfully.")