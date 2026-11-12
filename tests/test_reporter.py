import json
import numpy as np
import pytest

from src.dataset_analyzer.reporter import (
    generate_json_report,
    generate_html_report
)



def test_generate_json_report(tmp_path):
    inspection = {
        "rows": 5,
        "columns": 4,
        "duplicate_rows": 0
    }

    statistics = {
        "age": {
            "count": 5,
            "mean": 29.8
        }
    }

    outliers = {
        "age": {
            "outliers": []
        }
    }

    chart_paths = [tmp_path / "age_histogram.png"]

    output_file = tmp_path / "reports" / "report.json"

    result = generate_json_report(
        inspection,
        statistics,
        outliers,
        chart_paths,
        output_file
    )

    assert result.exists()

    with result.open("r", encoding="utf-8") as file:
        report = json.load(file)

    assert report["dataset_overview"]["rows"] == 5
    assert report["statistical_analysis"]["age"]["mean"] == 29.8
    assert report["charts"][0].endswith("age_histogram.png")
    assert "generated_at" in report


def test_json_report_handles_numpy_values(tmp_path):
    inspection = {
        "rows": np.int64(5)
    }

    statistics = {
        "age": {
            "mean": np.float64(29.5),
            "std": float("nan")
        }
    }

    output_file = tmp_path / "report.json"

    generate_json_report(
        inspection,
        statistics,
        {},
        [],
        output_file
    )

    with output_file.open("r", encoding="utf-8") as file:
        report = json.load(file)

    assert report["dataset_overview"]["rows"] == 5
    assert report["statistical_analysis"]["age"]["mean"] == 29.5
    assert report["statistical_analysis"]["age"]["std"] is None


def test_generate_json_report_creates_output_directory(tmp_path):
    output_file = tmp_path / "new_folder" / "report.json"

    generate_json_report({}, {}, {}, [], output_file)

    assert output_file.exists()


def test_generate_html_report_from_json(tmp_path):
    chart_file = tmp_path / "age_histogram.png"
    chart_file.write_bytes(b"fake image")

    report_data = {
        "generated_at": "2026-11-12T13:19:31+03:30",
        "dataset_overview": {
            "rows": 5,
            "columns": 4,
            "column_names": ["name", "age", "salary", "department"],
            "missing_values": {"age": 0},
            "duplicate_rows": 0
        },
        "statistical_analysis": {
            "age": {"mean": 29.8, "median": 29.0}
        },
        "outlier_analysis": {
            "age": {
                "lower_bound": 22.0,
                "upper_bound": 38.0,
                "outliers": []
            }
        },
        "charts": [str(chart_file)]
    }

    json_file = tmp_path / "report.json"

    with json_file.open("w", encoding="utf-8") as file:
        json.dump(report_data, file)

    output_file = tmp_path / "reports" / "report.html"

    result = generate_html_report(
        json_file=json_file,
        output_file=output_file
    )

    assert result.exists()

    html_content = result.read_text(encoding="utf-8")

    assert "Dataset Analysis Report" in html_content
    assert "Statistical Analysis" in html_content
    assert "29.8" in html_content
    assert "age_histogram.png" in html_content
    assert "2026-11-12T13:19:31+03:30" in html_content


def test_generate_html_report_creates_output_directory(tmp_path):
    json_file = tmp_path / "report.json"
    json_file.write_text("{}", encoding="utf-8")

    output_file = tmp_path / "new_folder" / "report.html"

    generate_html_report(
        json_file=json_file,
        output_file=output_file
    )

    assert output_file.exists()


def test_generate_html_report_json_not_found(tmp_path):
    json_file = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        generate_html_report(json_file=json_file)
