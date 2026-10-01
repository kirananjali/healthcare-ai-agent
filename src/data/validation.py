from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# 1. Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


# ---------------------------------------------------------
# 2. Load cleaned datasets
# ---------------------------------------------------------

patients = pd.read_csv(
    PROCESSED_DATA_DIR / "patients_cleaned.csv"
)

conditions = pd.read_csv(
    PROCESSED_DATA_DIR / "conditions_cleaned.csv"
)

medications = pd.read_csv(
    PROCESSED_DATA_DIR / "medications_cleaned.csv"
)

encounters = pd.read_csv(
    PROCESSED_DATA_DIR / "encounters_cleaned.csv"
)

observations = pd.read_csv(
    PROCESSED_DATA_DIR / "observations_cleaned.csv"
)

procedures = pd.read_csv(
    PROCESSED_DATA_DIR / "procedures_cleaned.csv"
)


# ---------------------------------------------------------
# 3. Helper function for validation output
# ---------------------------------------------------------

def print_validation_result(
    test_name: str,
    passed: bool,
) -> None:
    status = "PASS" if passed else "FAIL"

    print(f"{status}: {test_name}")


# ---------------------------------------------------------
# 4. Check required patient columns
# ---------------------------------------------------------

required_patient_columns = {
    "Id",
    "BIRTHDATE",
    "GENDER",
    "AGE",
}

required_columns_exist = (
    required_patient_columns.issubset(
        set(patients.columns)
    )
)

print_validation_result(
    "Required patient columns exist",
    required_columns_exist,
)


# ---------------------------------------------------------
# 5. Patient ID must not be missing
# ---------------------------------------------------------

patient_ids_not_missing = (
    patients["Id"]
    .notna()
    .all()
)

print_validation_result(
    "Patient IDs are not missing",
    patient_ids_not_missing,
)


# ---------------------------------------------------------
# 6. Patient IDs must be unique
# ---------------------------------------------------------

patient_ids_unique = (
    patients["Id"]
    .is_unique
)

print_validation_result(
    "Patient IDs are unique",
    patient_ids_unique,
)


# ---------------------------------------------------------
# 7. Validate patient age range
# ---------------------------------------------------------

valid_ages = (
    patients["AGE"]
    .dropna()
    .between(0, 120)
    .all()
)

print_validation_result(
    "Patient ages are between 0 and 120",
    valid_ages,
)


# ---------------------------------------------------------
# 8. Validate gender values
# ---------------------------------------------------------

allowed_gender_values = {
    "M",
    "F",
}

existing_gender_values = set(
    patients["GENDER"]
    .dropna()
    .unique()
)

gender_values_valid = (
    existing_gender_values.issubset(
        allowed_gender_values
    )
)

print_validation_result(
    "Gender values are valid",
    gender_values_valid,
)


# ---------------------------------------------------------
# 9. Create set of valid patient IDs
# ---------------------------------------------------------

valid_patient_ids = set(
    patients["Id"]
)


# ---------------------------------------------------------
# 10. Referential-integrity validation function
# ---------------------------------------------------------

def validate_patient_references(
    dataframe: pd.DataFrame,
    dataset_name: str,
) -> None:

    if "PATIENT" not in dataframe.columns:
        print_validation_result(
            f"{dataset_name} contains PATIENT column",
            False,
        )
        return

    referenced_patient_ids = set(
        dataframe["PATIENT"]
        .dropna()
    )

    invalid_patient_ids = (
        referenced_patient_ids
        - valid_patient_ids
    )

    passed = (
        len(invalid_patient_ids) == 0
    )

    print_validation_result(
        f"{dataset_name} patient references are valid",
        passed,
    )

    if not passed:
        print(
            "Invalid patient IDs found:",
            list(invalid_patient_ids)[:10],
        )


# ---------------------------------------------------------
# 11. Validate relationships
# ---------------------------------------------------------

validate_patient_references(
    conditions,
    "Conditions",
)

validate_patient_references(
    medications,
    "Medications",
)

validate_patient_references(
    encounters,
    "Encounters",
)

validate_patient_references(
    observations,
    "Observations",
)

validate_patient_references(
    procedures,
    "Procedures",
)


# ---------------------------------------------------------
# 12. Final summary
# ---------------------------------------------------------

print("\nValidation completed.")