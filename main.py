from src.dataset_analyzer.loader import load_csv
from src.dataset_analyzer.inspector import inspect_dataframe
from src.dataset_analyzer.statistics import calculate_statistics
from src.dataset_analyzer.outliers import detect_outliers


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