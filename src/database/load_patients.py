import pandas as pd

from src.data.data_loader import load_dataset
from src.database.connection import get_database_connection

def clean_database_value(value):
    """
    Convert Pandas missing values to Python None
    before sending values to PostgreSQL.
    """

    if pd.isna(value):
        return None

    return value

def load_patients_into_database():

    # Load the cleaned patients CSV into a Pandas DataFrame.
    patients = load_dataset(
        "patients",
        processed=True,
    )
    
    patients["BIRTHDATE"] = pd.to_datetime(
        patients["BIRTHDATE"],
        errors="coerce",
    ).dt.date

    patients["DEATHDATE"] = pd.to_datetime(
        patients["DEATHDATE"],
        errors="coerce",
    ).dt.date

    # Open a connection to PostgreSQL.
    connection = get_database_connection()

    try:

        # Create a cursor for executing SQL commands.
        with connection.cursor() as cursor:

            # Loop through every patient in the DataFrame.
            for _, patient in patients.iterrows():

                cursor.execute(
                    """
                    INSERT INTO patients (
                        id,
                        birthdate,
                        deathdate,
                        ssn,
                        drivers,
                        passport,
                        prefix,
                        first_name,
                        middle_name,
                        last_name,
                        suffix,
                        maiden,
                        marital,
                        race,
                        ethnicity,
                        gender,
                        birthplace,
                        address,
                        city,
                        state,
                        county,
                        fips,
                        zip,
                        latitude,
                        longitude,
                        healthcare_expenses,
                        healthcare_coverage,
                        income,
                        age
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s
                    )
                    ON CONFLICT (id) DO NOTHING;
                    """,
                    (
                        patient["Id"],
                        patient["BIRTHDATE"],
                        patient["DEATHDATE"],
                        patient["SSN"],
                        patient["DRIVERS"],
                        patient["PASSPORT"],
                        patient["PREFIX"],
                        patient["FIRST"],
                        patient["MIDDLE"],
                        patient["LAST"],
                        patient["SUFFIX"],
                        patient["MAIDEN"],
                        patient["MARITAL"],
                        patient["RACE"],
                        patient["ETHNICITY"],
                        patient["GENDER"],
                        patient["BIRTHPLACE"],
                        patient["ADDRESS"],
                        patient["CITY"],
                        patient["STATE"],
                        patient["COUNTY"],
                        patient["FIPS"],
                        patient["ZIP"],
                        patient["LAT"],
                        patient["LON"],
                        patient["HEALTHCARE_EXPENSES"],
                        patient["HEALTHCARE_COVERAGE"],
                        patient["INCOME"],
                        patient["AGE"],
                    ),
                )

        # Save all inserted records permanently.
        connection.commit()

        print(
            f"Successfully loaded {len(patients)} patients into PostgreSQL."
        )

    except Exception as error:

        # Undo the database changes if something fails.
        connection.rollback()

        print(
            f"Failed to load patients: {error}"
        )

        raise

    finally:

        # Always close the database connection.
        connection.close()


if __name__ == "__main__":

    load_patients_into_database()