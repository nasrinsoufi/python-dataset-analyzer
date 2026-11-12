import pandas as pd


def remove_duplicates(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from a DataFrame.

    Args:
        dataframe: The DataFrame to clean.

    Returns:
        A new DataFrame without duplicate rows.
    """
    return dataframe.drop_duplicates().copy()


def fill_missing_values(
    dataframe: pd.DataFrame,
    values: dict
) -> pd.DataFrame:
    """
    Fill missing values using the provided replacement values.

    Args:
        dataframe: The DataFrame to clean.
        values: A dictionary containing column names and replacement values.

    Returns:
        A new DataFrame with missing values filled.
    """
    return dataframe.fillna(value=values).copy()


def drop_missing_values(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows containing missing values.

    Args:
        dataframe: The DataFrame to clean.

    Returns:
        A new DataFrame without rows containing missing values.
    """
    return dataframe.dropna().copy()
