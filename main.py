from src.dataset_analyzer.loader import load_csv
from src.dataset_analyzer.inspector import inspect_dataframe
from src.dataset_analyzer.statistics import calculate_statistics


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
