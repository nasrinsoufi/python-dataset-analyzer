from datetime import datetime
import json
import math
from pathlib import Path
from typing import Any
import os
from html import escape


def _make_json_safe(value: Any) -> Any:
    """Convert values into types supported by JSON."""
    if isinstance(value, dict):
        return {
            str(key): _make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [_make_json_safe(item) for item in value]

    if isinstance(value, Path):
        return str(value)

    if hasattr(value, "item"):
        return _make_json_safe(value.item())

    if isinstance(value, float) and not math.isfinite(value):
        return None

    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    return str(value)


def generate_json_report(
    inspection: dict,
    statistics: dict,
    outliers: dict,
    chart_paths: list[str | Path],
    output_file: str | Path = "output/report.json"
) -> Path:
    """
    Generate a JSON report containing dataset analysis results.
    """
    report = {
        "generated_at": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "dataset_overview": inspection,
        "statistical_analysis": statistics,
        "outlier_analysis": outliers,
        "charts": [str(path) for path in chart_paths]
    }

    safe_report = _make_json_safe(report)

    file_path = Path(output_file)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(
            safe_report,
            file,
            indent=4,
            ensure_ascii=False,
            allow_nan=False
        )

    return file_path




def generate_html_report(
    json_file: str | Path,
    output_file: str | Path = "output/report.html"
    ) -> Path:
    """
    Generate an HTML report using an existing JSON report.
    """
    json_path = Path(json_file)

    if not json_path.exists():
        raise FileNotFoundError(f"JSON report not found: {json_path}")

    with json_path.open("r", encoding="utf-8") as file:
        report = json.load(file)

    # Extract data from JSON report
    inspection = report.get("dataset_overview", {})
    statistics = report.get("statistical_analysis", {})
    outliers = report.get("outlier_analysis", {})
    chart_paths = report.get("charts", [])

    file_path = Path(output_file)
    file_path.parent.mkdir(parents=True, exist_ok=True)


    # Dataset overview
    overview_rows = ""

    overview_items = {
        "Rows": inspection.get("rows", 0),
        "Columns": inspection.get("columns", 0),
        "Duplicate Rows": inspection.get("duplicate_rows", 0),
        "Column Names": ", ".join(
            str(name) for name in inspection.get("column_names", [])
        )
    }

    for label, value in overview_items.items():
        overview_rows += f"""
        <tr>
            <th>{escape(label)}</th>
            <td>{escape(str(value))}</td>
        </tr>
        """

    # Missing values
    missing_rows = ""

    for column, count in inspection.get("missing_values", {}).items():
        missing_rows += f"""
        <tr>
            <td>{escape(str(column))}</td>
            <td>{escape(str(count))}</td>
        </tr>
        """

    # Statistical analysis
    statistics_rows = ""

    for column, measures in statistics.items():
        for measure, value in measures.items():
            statistics_rows += f"""
            <tr>
                <td>{escape(str(column))}</td>
                <td>{escape(str(measure))}</td>
                <td>{escape(str(value))}</td>
            </tr>
            """

    # Outlier analysis
    outlier_rows = ""

    for column, result in outliers.items():
        detected = result.get("outliers", [])

        outlier_rows += f"""
        <tr>
            <td>{escape(str(column))}</td>
            <td>{escape(str(result.get("lower_bound", "")))}</td>
            <td>{escape(str(result.get("upper_bound", "")))}</td>
            <td>{escape(str(len(detected)))}</td>
        </tr>
        """

    # Charts
    chart_html = ""

    for chart_path in chart_paths:
        chart_path = Path(chart_path)

        relative_path = os.path.relpath(
            chart_path.resolve(),
            start=file_path.parent.resolve()
        ).replace("\\", "/")

        chart_html += f"""
        <div class="chart-card">
            <h3>{escape(chart_path.stem.replace("_", " ").title())}</h3>
            <img src="{escape(relative_path)}"
                 alt="{escape(chart_path.stem)}">
        </div>
        """

    generated_at = report.get("generated_at", "Unknown")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dataset Analysis Report</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f6f9;
                color: #263238;
                margin: 0;
                padding: 30px;
            }}

            .container {{
                max-width: 1100px;
                margin: auto;
            }}

            header {{
                background: #1e293b;
                color: white;
                padding: 25px;
                border-radius: 10px;
                margin-bottom: 25px;
            }}

            section {{
                background: white;
                padding: 25px;
                margin-bottom: 25px;
                border-radius: 10px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}

            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #e2e8f0;
            }}

            th {{
                background: #e2e8f0;
            }}

            .charts {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
            }}

            .chart-card {{
                border: 1px solid #e2e8f0;
                padding: 15px;
                border-radius: 8px;
            }}

            .chart-card img {{
                width: 100%;
                height: auto;
            }}

            footer {{
                text-align: center;
                color: #64748b;
                padding: 20px;
            }}
        </style>
    </head>

    <body>
        <div class="container">

            <header>
                <h1>Dataset Analysis Report</h1>
                <p>Generated at: {escape(generated_at)}</p>
            </header>

            <section>
                <h2>Dataset Overview</h2>
                <table>
                    <tbody>
                        {overview_rows}
                    </tbody>
                </table>
            </section>

            <section>
                <h2>Missing Values</h2>
                <table>
                    <tr>
                        <th>Column</th>
                        <th>Missing Count</th>
                    </tr>
                    {missing_rows}
                </table>
            </section>

            <section>
                <h2>Statistical Analysis</h2>
                <table>
                    <tr>
                        <th>Column</th>
                        <th>Measure</th>
                        <th>Value</th>
                    </tr>
                    {statistics_rows}
                </table>
            </section>

            <section>
                <h2>Outlier Analysis</h2>
                <table>
                    <tr>
                        <th>Column</th>
                        <th>Lower Bound</th>
                        <th>Upper Bound</th>
                        <th>Outlier Count</th>
                    </tr>
                    {outlier_rows}
                </table>
            </section>

            <section>
                <h2>Data Visualizations</h2>
                <div class="charts">
                    {chart_html}
                </div>
            </section>

            <footer>
                Generated by Python Dataset Analyzer
            </footer>

        </div>
    </body>
    </html>
    """

    file_path.write_text(html_content, encoding="utf-8")

    return file_path

