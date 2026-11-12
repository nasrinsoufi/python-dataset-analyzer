
import pandas as pd
import pytest

from src.dataset_analyzer.loader import load_csv


def test_load_csv_successfully(tmp_path):
    # Arrange
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age\nAli,28\nSara,32\n")

    # Act
    result = load_csv(csv_file)

    # Assert
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (2, 2)
    assert result.iloc[0]["name"] == "Ali"


def test_load_csv_file_not_found(tmp_path):
    csv_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_csv(csv_file)


def test_load_csv_wrong_extension(tmp_path):
    file = tmp_path / "data.txt"
    file.write_text("Hello")

    with pytest.raises(ValueError):
        load_csv(file)


def test_load_csv_empty_file(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")

    with pytest.raises(pd.errors.EmptyDataError):
        load_csv(csv_file)
