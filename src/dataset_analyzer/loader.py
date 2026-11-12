
from pathlib import Path

import pandas as pd


def load_csv(file_path: str | Path) -> pd.DataFrame:
    """
    Load a CSV file and return its contents as a pandas DataFrame.

    Args:
        file_path: Path to the CSV file.

    Returns:
        A pandas DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not CSV.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If the CSV structure is invalid.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise ValueError(f"The provided path is not a file: {path}")

    if path.suffix.lower() != ".csv":
        raise ValueError("Only CSV files are supported.")

    dataframe = pd.read_csv(path)

    return dataframe
