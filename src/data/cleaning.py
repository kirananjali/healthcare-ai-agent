from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# 1. Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


# ---------------------------------------------------------
# 2. Create processed directory if it does not exist
# ---------------------------------------------------------

PROCESSED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------------------------
# 3. Helper function to load and clean clinical datasets
# ---------------------------------------------------------

def load_and_clean_clinical_dataset(file_name: str) -> pd.DataFrame:
    """
    Load a clinical CSV file from data/raw and remove exact duplicate rows.
    """

    dataframe = pd.read_csv(
        RAW_DATA_DIR / file_name
    )

    dataframe = dataframe.drop_duplicates()

    return dataframe


# ---------------------------------------------------------
# 4. Load raw patients dataset
# ---------------------------------------------------------

patients = pd.read_csv(
    RAW_DATA_DIR / "patients.csv"
)


# ---------------------------------------------------------
# 5. Remove exact duplicate patient rows
# ---------------------------------------------------------

patients = patients.drop_duplicates()


# ---------------------------------------------------------
# 6. Remove duplicate patient IDs
# ---------------------------------------------------------

patients = patients.drop_duplicates(
    subset=["Id"]
)


# ---------------------------------------------------------
# 7. Convert patient date columns
# ---------------------------------------------------------

patients["BIRTHDATE"] = pd.to_datetime(
    patients["BIRTHDATE"],
    errors="coerce",
)

patients["DEATHDATE"] = pd.to_datetime(
    patients["DEATHDATE"],
    errors="coerce",
)


# ---------------------------------------------------------
# 8. Standardize patient text columns
# ---------------------------------------------------------

text_columns = [
    "FIRST",
    "LAST",
    "GENDER",
    "RACE",
    "ETHNICITY",
    "CITY",
    "STATE",
]

for column in text_columns:

    if column in patients.columns:

        patients[column] = (
            patients[column]
            .astype("string")
            .str.strip()
        )


# ---------------------------------------------------------
# 9. Standardize gender values
# ---------------------------------------------------------

if "GENDER" in patients.columns:

    patients["GENDER"] = (
        patients["GENDER"]
        .str.upper()
    )


# ---------------------------------------------------------
# 10. Calculate patient age
# ---------------------------------------------------------

REFERENCE_DATE = pd.Timestamp(
    "2026-09-01"
)

patients["AGE"] = (
    REFERENCE_DATE.year
    - patients["BIRTHDATE"].dt.year
)


# Adjust age if birthday has not occurred yet
birthday_not_reached = (
    (REFERENCE_DATE.month < patients["BIRTHDATE"].dt.month)
    |
    (
        (
            REFERENCE_DATE.month
            == patients["BIRTHDATE"].dt.month
        )
        &
        (
            REFERENCE_DATE.day
            < patients["BIRTHDATE"].dt.day
        )
    )
)

patients.loc[
    birthday_not_reached,
    "AGE",
] -= 1


# ---------------------------------------------------------
# 11. Detect invalid ages
# ---------------------------------------------------------

invalid_age_mask = (
    (patients["AGE"] < 0)
    |
    (patients["AGE"] > 120)
)

invalid_age_count = (
    invalid_age_mask.sum()
)

print(
    "Invalid age records:",
    invalid_age_count
)


# ---------------------------------------------------------
# 12. Replace invalid ages with missing values
# ---------------------------------------------------------

patients.loc[
    invalid_age_mask,
    "AGE",
] = pd.NA


# ---------------------------------------------------------
# 13. Load and clean all other clinical datasets
# ---------------------------------------------------------

conditions = load_and_clean_clinical_dataset(
    "conditions.csv"
)

medications = load_and_clean_clinical_dataset(
    "medications.csv"
)

encounters = load_and_clean_clinical_dataset(
    "encounters.csv"
)

observations = load_and_clean_clinical_dataset(
    "observations.csv"
)

procedures = load_and_clean_clinical_dataset(
    "procedures.csv"
)


# ---------------------------------------------------------
# 14. Save cleaned patients dataset
# ---------------------------------------------------------

patients.to_csv(
    PROCESSED_DATA_DIR / "patients_cleaned.csv",
    index=False,
)


# ---------------------------------------------------------
# 15. Save cleaned clinical datasets
# ---------------------------------------------------------

conditions.to_csv(
    PROCESSED_DATA_DIR / "conditions_cleaned.csv",
    index=False,
)

medications.to_csv(
    PROCESSED_DATA_DIR / "medications_cleaned.csv",
    index=False,
)

encounters.to_csv(
    PROCESSED_DATA_DIR / "encounters_cleaned.csv",
    index=False,
)

observations.to_csv(
    PROCESSED_DATA_DIR / "observations_cleaned.csv",
    index=False,
)

procedures.to_csv(
    PROCESSED_DATA_DIR / "procedures_cleaned.csv",
    index=False,
)


# ---------------------------------------------------------
# 16. Print summary
# ---------------------------------------------------------

print("\nCleaning completed successfully.")

print(
    "\nCleaned patients shape:",
    patients.shape
)

print(
    "Cleaned conditions shape:",
    conditions.shape
)

print(
    "Cleaned medications shape:",
    medications.shape
)

print(
    "Cleaned encounters shape:",
    encounters.shape
)

print(
    "Cleaned observations shape:",
    observations.shape
)

print(
    "Cleaned procedures shape:",
    procedures.shape
)


print("\nSample cleaned patient records:")

print(
    patients[
        [
            "Id",
            "BIRTHDATE",
            "FIRST",
            "LAST",
            "GENDER",
            "AGE",
        ]
    ].head()
)


print(
    "\nCleaned files saved under:",
    PROCESSED_DATA_DIR
)