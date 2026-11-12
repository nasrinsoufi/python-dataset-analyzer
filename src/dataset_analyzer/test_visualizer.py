import pandas as pd
import pytest

from src.dataset_analyzer.visualizer import (
    plot_histogram,
    plot_boxplot,
    plot_bar_chart
)


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "age": [20, 25, 30, 35, 40],
        "salary": [2000, 2500, 3000, 3500, 4000],
        "department": ["IT", "HR", "IT", "Finance", "HR"]
    })


def test_plot_histogram(sample_dataframe, tmp_path):
    result = plot_histogram(
        sample_dataframe,
        "age",
        tmp_path
    )

    assert result.exists()
    assert result.suffix == ".png"
    assert result.stat().st_size > 0


def test_plot_boxplot(sample_dataframe, tmp_path):
    result = plot_boxplot(
        sample_dataframe,
        "salary",
        tmp_path
    )

    assert result.exists()
    assert result.stat().st_size > 0


def test_plot_bar_chart(sample_dataframe, tmp_path):
    result = plot_bar_chart(
        sample_dataframe,
        "department",
        tmp_path
    )

    assert result.exists()
    assert result.stat().st_size > 0


def test_plot_with_nonexistent_column(sample_dataframe, tmp_path):
    with pytest.raises(ValueError):
        plot_histogram(
            sample_dataframe,
            "unknown",
            tmp_path
        )


def test_histogram_with_non_numeric_column(sample_dataframe, tmp_path):
    with pytest.raises(ValueError):
        plot_histogram(
            sample_dataframe,
            "department",
            tmp_path
        )
