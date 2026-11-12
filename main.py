import argparse
from pathlib import Path

from src.dataset_analyzer.loader import load_csv
from src.dataset_analyzer.inspector import inspect_dataframe
from src.dataset_analyzer.statistics import calculate_statistics
from src.dataset_analyzer.outliers import detect_outliers
from src.dataset_analyzer.visualizer import (
    plot_histogram,
    plot_boxplot,
    plot_bar_chart
)
from src.dataset_analyzer.reporter import (
    generate_json_report,
    generate_html_report
)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Analyze CSV datasets and generate reports."
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=Path("sample_data/sample.csv"),
        help="Path to the input CSV file."
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output"),
        help="Directory for generated charts and reports."
    )

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    # Load dataset
    data = load_csv(args.input)

    print("Dataset loaded successfully!")
    print(f"Input file: {args.input}")

    # Inspect dataset
    inspection = inspect_dataframe(data)

    print("\nDataset Inspection:")
    for key, value in inspection.items():
        print(f"{key}: {value}")

    # Statistical analysis
    statistics = calculate_statistics(data)

    print("\nStatistical Analysis:")
    for column, measures in statistics.items():
        print(f"\nColumn: {column}")

        for measure, value in measures.items():
            if measure == "count":
                print(f"  {measure}: {value}")
            else:
                print(f"  {measure}: {value:.2f}")

    # Detect outliers
    outlier_results = detect_outliers(data)

    print("\nOutlier Detection:")

    for column, result in outlier_results.items():
        print(f"\nColumn: {column}")
        print(f"Lower Bound: {result['lower_bound']:.2f}")
        print(f"Upper Bound: {result['upper_bound']:.2f}")
        print(f"Outliers: {result['outliers']}")

    # Create charts
    histogram_path = plot_histogram(
        data, "age", output_dir=args.output
    )

    boxplot_path = plot_boxplot(
        data, "salary", output_dir=args.output
    )

    bar_chart_path = plot_bar_chart(
        data, "department", output_dir=args.output
    )

    chart_paths = [
        histogram_path,
        boxplot_path,
        bar_chart_path
    ]

    print("\nGenerated Charts:")
    for chart_path in chart_paths:
        print(chart_path)

    # Generate JSON report
    json_report_path = generate_json_report(
        inspection=inspection,
        statistics=statistics,
        outliers=outlier_results,
        chart_paths=chart_paths,
        output_file=args.output / "report.json"
    )

    print("\nJSON Report Generated:")
    print(json_report_path)

    # Generate HTML report from JSON
    html_report_path = generate_html_report(
        json_file=json_report_path,
        output_file=args.output / "report.html"
    )

    print("\nHTML Report Generated:")
    print(html_report_path)


if __name__ == "__main__":
    main()
