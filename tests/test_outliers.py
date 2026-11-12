import pandas as pd
import pytest

from src.dataset_analyzer.outliers import detect_outliers


def test_detect_outliers():
    dataframe = pd.DataFrame({
        "salary": [10, 12, 13, 14, 15, 100]
    })

    result = detect_outliers(dataframe)

    assert len(result["salary"]["outliers"]) == 1
    assert result["salary"]["outliers"][0]["value"] == 100


def test_no_outliers():
    dataframe = pd.DataFrame({
        "salary": [10, 12, 13, 14, 15]
    })

    result = detect_outliers(dataframe)

    assert result["salary"]["outliers"] == []


def test_ignore_non_numeric_columns():
    dataframe = pd.DataFrame({
        "name": ["Ali", "Sara", "Reza"],
        "age": [20, 25, 30]
    })

    result = detect_outliers(dataframe)

    assert "name" not in result
    assert "age" in result


def test_detect_outliers_with_missing_values():
    dataframe = pd.DataFrame({
        "salary": [10, 12, None, 14, 15, 100]
    })

    result = detect_outliers(dataframe)

    assert len(result["salary"]["outliers"]) == 1
    assert result["salary"]["outliers"][0]["value"] == 100


def test_invalid_multiplier():
    dataframe = pd.DataFrame({
        "salary": [10, 20, 30]
    })

    with pytest.raises(ValueError):
        detect_outliers(dataframe, multiplier=0)
