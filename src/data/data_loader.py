from pathlib import Path
import logging

import pandas as pd


# ---------------------------------------------------------
# 1. Configure logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# 2. Define project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


# ---------------------------------------------------------
# 3. Define datasets supported by the project
# ---------------------------------------------------------

SUPPORTED_DATASETS = {
    "patients",
    "conditions",
    "medications",
    "encounters",
    "observations",
    "procedures",
}


# ---------------------------------------------------------
# 4. Reusable function to load one dataset
# ---------------------------------------------------------

def load_dataset(
    dataset_name: str,
    processed: bool = False,
) -> pd.DataFrame:
    """
    Load one healthcare dataset.

    Args:
        dataset_name:
            Name of the dataset, for example "patients".

        processed:
            False loads data/raw.
            True loads data/processed.

    Returns:
        A Pandas DataFrame containing the dataset.

    Raises:
        ValueError:
            If an unsupported dataset name is provided.

        FileNotFoundError:
            If the expected CSV file does not exist.

        RuntimeError:
            If Pandas cannot read the CSV file.
    """

    # Standardize the dataset name.
    dataset_name = dataset_name.lower().strip()

    # Validate that the requested dataset is supported.
    if dataset_name not in SUPPORTED_DATASETS:
        raise ValueError(
            f"Unsupported dataset: {dataset_name}. "
            f"Supported datasets: {sorted(SUPPORTED_DATASETS)}"
        )

    # Decide whether to use raw or processed data.
    if processed:
        data_directory = PROCESSED_DATA_DIR
        file_name = f"{dataset_name}_cleaned.csv"
    else:
        data_directory = RAW_DATA_DIR
        file_name = f"{dataset_name}.csv"

    # Build the complete path to the CSV file.
    file_path = data_directory / file_name

    # Validate that the file actually exists.
    if not file_path.exists():
        logger.error(
            "Dataset file was not found: %s",
            file_path,
        )

        raise FileNotFoundError(
            f"Dataset file not found: {file_path}"
        )

    # Attempt to read the CSV file.
    try:
        dataframe = pd.read_csv(file_path)

    except Exception as error:
        logger.exception(
            "Failed to load dataset '%s'.",
            dataset_name,
        )

        raise RuntimeError(
            f"Failed to load dataset: {dataset_name}"
        ) from error

    # Record successful ingestion.
    logger.info(
        "Loaded '%s' with %d rows and %d columns.",
        dataset_name,
        dataframe.shape[0],
        dataframe.shape[1],
    )

    return dataframe


# ---------------------------------------------------------
# 5. Reusable function to load all datasets
# ---------------------------------------------------------

def load_all_datasets(
    processed: bool = False,
) -> dict[str, pd.DataFrame]:
    """
    Load all supported healthcare datasets.

    Returns:
        Dictionary where:
        key   = dataset name
        value = Pandas DataFrame
    """

    datasets = {}

    for dataset_name in sorted(SUPPORTED_DATASETS):

        datasets[dataset_name] = load_dataset(
            dataset_name=dataset_name,
            processed=processed,
        )

    return datasets


# ---------------------------------------------------------
# 6. Test the loader when this file is executed directly
# ---------------------------------------------------------

if __name__ == "__main__":

    logger.info(
        "Starting healthcare data ingestion test."
    )


    raw_datasets = load_all_datasets(
        processed=False
    )

    print("\nSuccessfully loaded raw datasets:")

    for dataset_name, dataframe in raw_datasets.items():
        print(
            f"{dataset_name}: "
            f"{dataframe.shape[0]} rows, "
            f"{dataframe.shape[1]} columns"
        )

    logger.info(
        "Healthcare data ingestion test completed."
    )

     