import pandas as pd

from src.dataset_analyzer.inspector import inspect_dataframe


def test_inspect_dataframe_basic_information():
    # Arrange
    dataframe = pd.DataFrame({
        "name": ["Ali", "Sara", "Reza"],
        "age": [28, 32, 25],
        "salary": [2500, 3200, 2200]
    })

    # Act
    result = inspect_dataframe(dataframe)

    # Assert
    assert result["rows"] == 3
    assert result["columns"] == 3
    assert result["column_names"] == ["name", "age", "salary"]
    assert result["duplicate_rows"] == 0


def test_inspect_dataframe_missing_values():
    # Arrange
    dataframe = pd.DataFrame({
        "name": ["Ali", "Sara", None],
        "age": [28, None, 25]
    })

    # Act
    result = inspect_dataframe(dataframe)

    # Assert
    assert result["missing_values"]["name"] == 1
    assert result["missing_values"]["age"] == 1


def test_inspect_dataframe_duplicate_rows():
    # Arrange
    dataframe = pd.DataFrame({
        "name": ["Ali", "Sara", "Ali"],
        "age": [28, 32, 28]
    })

    # Act
    result = inspect_dataframe(dataframe)

    # Assert
    assert result["duplicate_rows"] == 1


def test_inspect_empty_dataframe():
    # Arrange
    dataframe = pd.DataFrame()

    # Act
    result = inspect_dataframe(dataframe)

    # Assert
    assert result["rows"] == 0
    assert result["columns"] == 0
    assert result["duplicate_rows"] == 0
