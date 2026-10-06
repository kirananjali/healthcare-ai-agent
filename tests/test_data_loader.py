import sys
from pathlib import Path

import pandas as pd
import pytest


# ---------------------------------------------------------
# 1. Make the project root importable
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT),
)


# ---------------------------------------------------------
# 2. Import functions we want to test
# ---------------------------------------------------------

from src.data.data_loader import (
    SUPPORTED_DATASETS,
    load_all_datasets,
    load_dataset,
)


# ---------------------------------------------------------
# 3. Test loading one valid dataset
# ---------------------------------------------------------

def test_load_patients_dataset():

    patients = load_dataset(
        "patients"
    )

    assert isinstance(
        patients,
        pd.DataFrame,
    )

    assert not patients.empty

    assert "Id" in patients.columns


# ---------------------------------------------------------
# 4. Test dataset-name normalization
# ---------------------------------------------------------

def test_dataset_name_normalization():

    patients = load_dataset(
        "  PATIENTS  "
    )

    assert isinstance(
        patients,
        pd.DataFrame,
    )

    assert not patients.empty


# ---------------------------------------------------------
# 5. Test unsupported dataset
# ---------------------------------------------------------

def test_invalid_dataset_name():

    with pytest.raises(
        ValueError
    ):
        load_dataset(
            "abc"
        )


# ---------------------------------------------------------
# 6. Test loading processed data
# ---------------------------------------------------------

def test_load_processed_patients():

    patients = load_dataset(
        "patients",
        processed=True,
    )

    assert isinstance(
        patients,
        pd.DataFrame,
    )

    assert not patients.empty

    assert "AGE" in patients.columns


# ---------------------------------------------------------
# 7. Test loading all datasets
# ---------------------------------------------------------

def test_load_all_datasets():

    datasets = load_all_datasets()

    assert set(
        datasets.keys()
    ) == SUPPORTED_DATASETS

    for dataframe in datasets.values():

        assert isinstance(
            dataframe,
            pd.DataFrame,
        )

        assert not dataframe.empty