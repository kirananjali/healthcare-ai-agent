from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# 1. Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# ---------------------------------------------------------
# 2. Load datasets
# ---------------------------------------------------------

patients = pd.read_csv(RAW_DATA_DIR / "patients.csv")
conditions = pd.read_csv(RAW_DATA_DIR / "conditions.csv")
medications = pd.read_csv(RAW_DATA_DIR / "medications.csv")
encounters = pd.read_csv(RAW_DATA_DIR / "encounters.csv")
observations = pd.read_csv(RAW_DATA_DIR / "observations.csv")
procedures = pd.read_csv(RAW_DATA_DIR / "procedures.csv")


# ---------------------------------------------------------
# 3. Store datasets in a dictionary
# ---------------------------------------------------------

datasets = {
    "patients": patients,
    "conditions": conditions,
    "medications": medications,
    "encounters": encounters,
    "observations": observations,
    "procedures": procedures,
}


# ---------------------------------------------------------
# 4. Basic dataset information
# ---------------------------------------------------------

print("\n================ DATASET SUMMARY ================\n")

for dataset_name, dataframe in datasets.items():
    print(
        f"{dataset_name}: "
        f"{dataframe.shape[0]} rows, "
        f"{dataframe.shape[1]} columns"
    )


# ---------------------------------------------------------
# 5. Display columns for every dataset
# ---------------------------------------------------------

print("\n================ DATASET COLUMNS ================\n")

for dataset_name, dataframe in datasets.items():
    print(f"\n{dataset_name.upper()}")

    for column in dataframe.columns:
        print(f"  - {column}")


# ---------------------------------------------------------
# 6. Check missing values
# ---------------------------------------------------------

print("\n================ MISSING VALUES ================\n")

for dataset_name, dataframe in datasets.items():

    missing_values = dataframe.isnull().sum()

    missing_values = missing_values[
        missing_values > 0
    ]

    print(f"\n{dataset_name.upper()}")

    if missing_values.empty:
        print("No missing values found.")
    else:
        print(missing_values)


# ---------------------------------------------------------
# 7. Check duplicate rows
# ---------------------------------------------------------

print("\n================ DUPLICATES ================\n")

for dataset_name, dataframe in datasets.items():

    duplicate_count = dataframe.duplicated().sum()

    print(
        f"{dataset_name}: "
        f"{duplicate_count} duplicate rows"
    )


# ---------------------------------------------------------
# 8. Check duplicate patient IDs
# ---------------------------------------------------------

duplicate_patient_ids = patients["Id"].duplicated().sum()

print(
    "\nDuplicate patient IDs:",
    duplicate_patient_ids
)


# ---------------------------------------------------------
# 9. Select one patient
# ---------------------------------------------------------

selected_patient_id = patients.iloc[0]["Id"]

print(
    "\nSelected patient ID:",
    selected_patient_id
)


# ---------------------------------------------------------
# 10. Retrieve patient demographic record
# ---------------------------------------------------------

selected_patient = patients[
    patients["Id"] == selected_patient_id
]

print("\n================ PATIENT ================\n")

print(
    selected_patient[
        [
            "Id",
            "BIRTHDATE",
            "FIRST",
            "LAST",
            "GENDER",
            "CITY",
            "STATE",
        ]
    ]
)


# ---------------------------------------------------------
# 11. Retrieve patient's related clinical records
# ---------------------------------------------------------

patient_conditions = conditions[
    conditions["PATIENT"] == selected_patient_id
]

patient_medications = medications[
    medications["PATIENT"] == selected_patient_id
]

patient_encounters = encounters[
    encounters["PATIENT"] == selected_patient_id
]

patient_observations = observations[
    observations["PATIENT"] == selected_patient_id
]

patient_procedures = procedures[
    procedures["PATIENT"] == selected_patient_id
]


# ---------------------------------------------------------
# 12. Print counts for selected patient
# ---------------------------------------------------------

print("\n================ PATIENT RECORD COUNTS ================\n")

print(
    "Conditions:",
    len(patient_conditions)
)

print(
    "Medications:",
    len(patient_medications)
)

print(
    "Encounters:",
    len(patient_encounters)
)

print(
    "Observations:",
    len(patient_observations)
)

print(
    "Procedures:",
    len(patient_procedures)
)


# ---------------------------------------------------------
# 13. Display sample related records
# ---------------------------------------------------------

print("\n================ CONDITIONS ================\n")
print(patient_conditions.head())

print("\n================ MEDICATIONS ================\n")
print(patient_medications.head())

print("\n================ ENCOUNTERS ================\n")
print(patient_encounters.head())

print("\n================ OBSERVATIONS ================\n")
print(patient_observations.head())

print("\n================ PROCEDURES ================\n")
print(patient_procedures.head())