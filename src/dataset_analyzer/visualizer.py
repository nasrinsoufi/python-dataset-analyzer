from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def _validate_column(
    dataframe: pd.DataFrame,
    column: str,
    numeric_only: bool = False
) -> None:
    """Validate that the requested column exists and has the expected type."""

    if column not in dataframe.columns:
        raise ValueError(f"Column '{column}' does not exist.")

    if numeric_only and not pd.api.types.is_numeric_dtype(dataframe[column]):
        raise ValueError(f"Column '{column}' must be numeric.")

    if dataframe[column].dropna().empty:
        raise ValueError(f"Column '{column}' contains no valid data.")


def plot_histogram(
    dataframe: pd.DataFrame,
    column: str,
    output_dir: str | Path = "output"
) -> Path:
    """
    Create and save a histogram for a numeric column.

    Returns:
        The path of the generated chart.
    """

    _validate_column(dataframe, column, numeric_only=True)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(dataframe[column].dropna(), bins=10, edgecolor="black")
    ax.set_title(f"Distribution of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")

    fig.tight_layout()

    file_path = output_path / f"{column}_histogram.png"
    fig.savefig(file_path, dpi=150)
    plt.close(fig)

    return file_path


def plot_boxplot(
    dataframe: pd.DataFrame,
    column: str,
    output_dir: str | Path = "output"
) -> Path:
    """
    Create and save a box plot for a numeric column.

    Returns:
        The path of the generated chart.
    """

    _validate_column(dataframe, column, numeric_only=True)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.boxplot(dataframe[column].dropna())
    ax.set_title(f"Box Plot of {column}")
    ax.set_ylabel(column)

    fig.tight_layout()

    file_path = output_path / f"{column}_boxplot.png"
    fig.savefig(file_path, dpi=150)
    plt.close(fig)

    return file_path


def plot_bar_chart(
    dataframe: pd.DataFrame,
    column: str,
    output_dir: str | Path = "output"
) -> Path:
    """
    Create and save a bar chart showing category frequencies.

    Returns:
        The path of the generated chart.
    """

    _validate_column(dataframe, column)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    frequencies = dataframe[column].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))

    frequencies.plot(kind="bar", ax=ax)
    ax.set_title(f"Frequency of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Count")

    fig.tight_layout()

    file_path = output_path / f"{column}_bar_chart.png"
    fig.savefig(file_path, dpi=150)
    plt.close(fig)

    return file_path
