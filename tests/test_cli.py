from pathlib import Path

import pytest
import main as cli


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
