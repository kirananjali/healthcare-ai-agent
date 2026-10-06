from src.database.connection import get_database_connection


def test_database_connection():

    connection = get_database_connection()

    with connection.cursor() as cursor:

        cursor.execute(
            "SELECT current_database();"
        )

        database_name = cursor.fetchone()[0]

    connection.close()

    assert database_name == "healthcare_ai"