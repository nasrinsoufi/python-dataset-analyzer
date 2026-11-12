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

data = load_csv("sample_data/sample.csv")

print("Dataset loaded successfully!")

inspection = inspect_dataframe(data)

print("\nDataset Inspection:")
for key, value in inspection.items():
    print(f"{key}: {value}")


statistics = calculate_statistics(data)

print("\nStatistical Analysis:")
for column, measures in statistics.items():
    print(f"\nColumn: {column}")

    for measure, value in measures.items():
        print(f"  {measure}: {value:.2f}" if measure != "count" else f"  {measure}: {value}")


outlier_results = detect_outliers(data)

print("\nOutlier Detection:")

for column, result in outlier_results.items():
    print(f"\nColumn: {column}")
    print(f"Lower Bound: {result['lower_bound']:.2f}")
    print(f"Upper Bound: {result['upper_bound']:.2f}")
    print(f"Outliers: {result['outliers']}")


# Create charts
histogram_path = plot_histogram(data, "age")
boxplot_path = plot_boxplot(data, "salary")
bar_chart_path = plot_bar_chart(data, "department")

print("\nGenerated Charts:")
print(histogram_path)
print(boxplot_path)
print(bar_chart_path)


# Generate JSON report
chart_paths = [
    histogram_path,
    boxplot_path,
    bar_chart_path
]

json_report_path = generate_json_report(
    inspection=inspection,
    statistics=statistics,
    outliers=outlier_results,
    chart_paths=chart_paths
)

print("\nJSON Report Generated:")
print(json_report_path)


# Generate HTML report
html_report_path = generate_html_report(
    json_file=json_report_path
)

print("\nHTML Report Generated:")
print(html_report_path)