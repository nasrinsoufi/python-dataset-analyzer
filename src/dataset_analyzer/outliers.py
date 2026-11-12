import pandas as pd


def detect_outliers(
    dataframe: pd.DataFrame,
    multiplier: float = 1.5
) -> dict:
    """
    Detect outliers in numeric columns using the IQR method.

    Args:
        dataframe: The DataFrame to analyze.
        multiplier: The IQR multiplier used to calculate the boundaries.

    Returns:
        A dictionary containing outlier information for each numeric column.

    Raises:
        ValueError: If the multiplier is not positive.
    """

    if multiplier <= 0:
        raise ValueError("Multiplier must be greater than zero.")

    numeric_dataframe = dataframe.select_dtypes(include="number")

    results = {}

    for column in numeric_dataframe.columns:
        series = numeric_dataframe[column].dropna()

        if series.empty:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr

        outliers = series[
            (series < lower_bound) |
            (series > upper_bound)
        ]

        results[column] = {
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound),
            "outliers": [
                {
                    "index": index,
                    "value": value.item()
                    if hasattr(value, "item") else value
                }
                for index, value in outliers.items()
            ]
        }

    return results
