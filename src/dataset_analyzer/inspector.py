import pandas as pd


def inspect_dataframe(dataframe: pd.DataFrame) -> dict:
    """
    Inspect a DataFrame and return its basic information.

    Args:
        dataframe: The DataFrame to inspect.

    Returns:
        A dictionary containing dataset information.
    """

    inspection = {
        "rows": dataframe.shape[0],
        "columns": dataframe.shape[1],
        "column_names": list(dataframe.columns),
        "data_types": dataframe.dtypes.astype(str).to_dict(),
        "missing_values": dataframe.isnull().sum().to_dict(),
        "duplicate_rows": int(dataframe.duplicated().sum()),
    }

    return inspection
