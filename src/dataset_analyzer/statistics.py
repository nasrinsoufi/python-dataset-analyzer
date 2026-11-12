import pandas as pd


def calculate_statistics(dataframe: pd.DataFrame) -> dict:
    """
    Calculate descriptive statistics for numeric columns.

    Args:
        dataframe: The DataFrame to analyze.

    Returns:
        A dictionary containing statistical measures for each numeric column.
    """

    numeric_dataframe = dataframe.select_dtypes(include="number")

    statistics = {}

    for column in numeric_dataframe.columns:
        series = numeric_dataframe[column]

        statistics[column] = {
            "count": int(series.count()),
            "mean": float(series.mean()),
            "median": float(series.median()),
            "std": float(series.std()),
            "min": float(series.min()),
            "max": float(series.max())
        }

    return statistics
