from src.dataset_analyzer.loader import load_csv


data = load_csv("sample_data/sample.csv")

print("Dataset loaded successfully!")
print(data)
print("\nDataset shape:", data.shape)
