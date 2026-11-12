import pandas as pd

from src.dataset_analyzer.cleaner import (
    remove_duplicates,
    fill_missing_values,
    drop_missing_values
)


def test_remove_duplicates():
    dataframe = pd.DataFrame({
        "name": ["Ali", "Sara", "Ali"],
        "age": [28, 32, 28]
    })

    result = remove_duplicates(dataframe)

    assert len(result) == 2
    assert len(dataframe) == 3


def test_fill_missing_values():
    dataframe = pd.DataFrame({
        "name": ["Ali", None],
        "age": [28, None]
    })

    result = fill_missing_values(
        dataframe,
        {"name": "Unknown", "age": 0}
    )

    assert result["name"].isnull().sum() == 0
    assert result["age"].isnull().sum() == 0
    assert result.iloc[1]["name"] == "Unknown"
    assert result.iloc[1]["age"] == 0


def test_drop_missing_values():
    dataframe = pd.DataFrame({
        "name": ["Ali", "Sara", None],
        "age": [28, None, 25]
    })

    result = drop_missing_values(dataframe)

    assert len(result) == 1
    assert result.isnull().sum().sum() == 0


def test_cleaning_does_not_modify_original_dataframe():
    dataframe = pd.DataFrame({
        "name": ["Ali", "Ali"],
        "age": [28, 28]
    })

    result = remove_duplicates(dataframe)

    assert len(dataframe) == 2
    assert len(result) == 1
