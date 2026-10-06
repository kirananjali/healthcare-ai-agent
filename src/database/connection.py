import os

import psycopg
from dotenv import load_dotenv


# Load environment variables from the .env file.
load_dotenv()


# Read PostgreSQL connection settings.
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_database_connection():
    """
    Create and return a connection to PostgreSQL.
    """

    connection = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    return connection


if __name__ == "__main__":

    try:

        connection = get_database_connection()

        print(
            "Successfully connected to PostgreSQL."
        )

        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT current_database();"
            )

            database_name = cursor.fetchone()[0]

            print(
                f"Connected database: {database_name}"
            )

        connection.close()

        print(
            "Database connection closed."
        )

    except Exception as error:

        print(
            f"Database connection failed: {error}"
        )