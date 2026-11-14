from pathlib import Path

import pytest
import main as cli
import json


def test_cli_default_arguments():
    parser = cli.build_parser()
    args = parser.parse_args([])

    assert args.input == Path("sample_data/sample.csv")
    assert args.output == Path("output")


def test_cli_custom_arguments():
    parser = cli.build_parser()

    args = parser.parse_args([
        "--input", "data/custom.csv",
        "--output", "results"
    ])

    assert args.input == Path("data/custom.csv")
    assert args.output == Path("results")


def test_cli_help(capsys):
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--help"])

    assert exc_info.value.code == 0

    captured = capsys.readouterr()
    assert "--input" in captured.out
    assert "--output" in captured.out


def test_main_runs_analysis_pipeline(monkeypatch, tmp_path):
    input_file = tmp_path / "sample.csv"
    output_dir = tmp_path / "results"

    dummy_data = object()

    inspection = {"rows": 5, "columns": 4}
    statistics = {"age": {"mean": 29.8}}
    outliers = {
    "age": {
        "lower_bound": 22.0,
        "upper_bound": 38.0,
        "outliers": []
    }
}

    monkeypatch.setattr(
        cli, "load_csv",
        lambda path: dummy_data
    )

    monkeypatch.setattr(
        cli, "inspect_dataframe",
        lambda data: inspection
    )

    monkeypatch.setattr(
        cli, "calculate_statistics",
        lambda data: statistics
    )

    monkeypatch.setattr(
        cli, "detect_outliers",
        lambda data: outliers
    )

    monkeypatch.setattr(
        cli, "plot_histogram",
        lambda data, column, output_dir:
            output_dir / "age_histogram.png"
    )

    monkeypatch.setattr(
        cli, "plot_boxplot",
        lambda data, column, output_dir:
            output_dir / "salary_boxplot.png"
    )

    monkeypatch.setattr(
        cli, "plot_bar_chart",
        lambda data, column, output_dir:
            output_dir / "department_bar_chart.png"
    )

    monkeypatch.setattr(
        cli, "generate_json_report",
        lambda **kwargs: kwargs["output_file"]
    )

    monkeypatch.setattr(
        cli, "generate_html_report",
        lambda **kwargs: kwargs["output_file"]
    )

    cli.main([
        "--input", str(input_file),
        "--output", str(output_dir)
    ])


def test_main_raises_error_for_missing_input(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        cli.main([
            "--input", str(missing_file),
            "--output", str(tmp_path / "results")
        ])


def test_cli_end_to_end(tmp_path):
    input_file = tmp_path / "input.csv"
    output_dir = tmp_path / "results"

    csv_content = """name,age,salary,department
Ali,28,2500,IT
Sara,32,3200,HR
Reza,25,2200,IT
Mina,35,4100,Finance
Nima,29,3000,Marketing
"""

    input_file.write_text(csv_content, encoding="utf-8")

    cli.main([
        "--input", str(input_file),
        "--output", str(output_dir)
    ])

    expected_files = [
        "age_histogram.png",
        "salary_boxplot.png",
        "department_bar_chart.png",
        "report.json",
        "report.html"
    ]

    for filename in expected_files:
        assert (output_dir / filename).is_file()

    report_path = output_dir / "report.json"

    with report_path.open("r", encoding="utf-8") as file:
        report = json.load(file)

    assert report["dataset_overview"]["rows"] == 5
    assert report["dataset_overview"]["columns"] == 4

    assert report["statistical_analysis"]["age"]["mean"] == pytest.approx(29.8)

    assert len(report["charts"]) == 3

    html_content = (
        output_dir / "report.html"
    ).read_text(encoding="utf-8")

    assert "age_histogram.png" in html_content