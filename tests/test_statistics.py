import pandas as pd

from src.dataset_analyzer.statistics import calculate_statistics


def test_calculate_statistics():
    dataframe = pd.DataFrame({
        "age": [20, 30, 40],
        "salary": [2000, 3000, 4000],
        "name": ["Ali", "Sara", "Reza"]
    })

    result = calculate_statistics(dataframe)

    assert result["age"]["count"] == 3
    assert result["age"]["mean"] == 30
    assert result["age"]["median"] == 30
    assert result["age"]["min"] == 20
    assert result["age"]["max"] == 40

    assert result["salary"]["mean"] == 3000

    assert "name" not in result


def test_statistics_with_missing_values():
    dataframe = pd.DataFrame({
        "age": [20, None, 40]
    })

    result = calculate_statistics(dataframe)

    assert result["age"]["count"] == 2
    assert result["age"]["mean"] == 30


def test_statistics_without_numeric_columns():
    dataframe = pd.DataFrame({
        "name": ["Ali", "Sara"],
        "department": ["IT", "HR"]
    })

    result = calculate_statistics(dataframe)

    assert result == {}


def test_statistics_with_empty_dataframe():
    dataframe = pd.DataFrame()

    result = calculate_statistics(dataframe)

    assert result == {}
