# Python Dataset Analyzer

A Python-based command-line tool for analyzing CSV datasets, calculating statistical summaries, detecting outliers, generating visualizations, and producing JSON and HTML reports.

The project is designed with a modular structure, making its components reusable, testable, and easy to extend.

## Features

- **CSV Data Loading:** Load CSV files and validate input paths and file formats.
- **Dataset Inspection:** Explore dataset dimensions, column names, data types, missing values, and duplicate rows.
- **Data Cleaning:** Remove duplicate rows, fill missing values, or drop rows containing missing values.
- **Statistical Analysis:** Calculate count, mean, median, standard deviation, minimum, and maximum for numerical columns.
- **Outlier Detection:** Identify potential outliers using the Interquartile Range (IQR) method.
- **Data Visualization:** Generate histograms, box plots, and bar charts.
- **JSON Reporting:** Export analysis results into structured JSON reports.
- **HTML Reporting:** Generate readable HTML reports using the JSON report as the single source of truth.
- **Command-Line Interface:** Run the analysis pipeline with custom input and output paths.
- **Automated Testing:** Validate individual modules and the complete analysis pipeline using pytest.

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Argparse
- Pytest

## Project Structure

```text
python-dataset-analyzer/
│
├── src/
│   └── dataset_analyzer/
│       ├── __init__.py
│       ├── loader.py
│       ├── inspector.py
│       ├── cleaner.py
│       ├── statistics.py
│       ├── outliers.py
│       ├── visualizer.py
│       └── reporter.py
│
├── tests/
│   ├── test_loader.py
│   ├── test_inspector.py
│   ├── test_cleaner.py
│   ├── test_statistics.py
│   ├── test_outliers.py
│   ├── test_visualizer.py
│   ├── test_reporter.py
│   └── test_cli.py
│
├── sample_data/
│   └── sample.csv
│
├── output/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/nasrinsoufi/python-dataset-analyzer.git
cd python-dataset-analyzer
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Usage

### Run with the default dataset

```bash
python main.py
```

By default, the application uses:

- Input: `sample_data/sample.csv`
- Output: `output/`

### Run with a custom CSV file

```bash
python main.py --input path/to/your_dataset.csv --output results
```

### View available command-line options

```bash
python main.py --help
```

Available arguments:

| Argument | Description | Default |
|---|---|---|
| `--input` | Path to the input CSV file | `sample_data/sample.csv` |
| `--output` | Directory for generated charts and reports | `output` |

## Output Files

After a successful execution, the application generates the following files:

```text
output/
├── age_histogram.png
├── salary_boxplot.png
├── department_bar_chart.png
├── report.json
└── report.html
```

### Visualizations

The application generates three types of charts:

- **Histogram:** Displays the distribution of numerical values.
- **Box Plot:** Visualizes data distribution and potential outliers.
- **Bar Chart:** Shows the frequency of categorical values.

### JSON Report

The JSON report contains:

- Dataset overview
- Column data types
- Missing value counts
- Duplicate row count
- Statistical analysis
- Outlier detection results
- Generated chart paths
- Report generation timestamp

### HTML Report

The HTML report presents the analysis results in a structured and readable format, including statistical tables, outlier information, dataset overview, and chart references.

The HTML report is generated from the JSON report to maintain a consistent source of analysis data.

## Outlier Detection

The project uses the Interquartile Range (IQR) method to identify potential outliers.

The IQR is calculated as:

```text
IQR = Q3 - Q1
```

The default boundaries are:

```text
Lower Bound = Q1 - 1.5 * IQR
Upper Bound = Q3 + 1.5 * IQR
```

Values outside these boundaries are identified as potential outliers.

The detection process does not automatically remove outliers from the dataset.

## Running Tests

The project uses pytest for automated testing.

Run all tests:

```bash
python -m pytest -v
```

The test suite covers individual modules, error handling, command-line arguments, and end-to-end execution of the analysis pipeline.

## Current Scope and Limitations

- CSV files are currently supported as input.
- Statistical analysis is performed on numerical columns.
- The CLI visualization pipeline currently expects the columns `age`, `salary`, and `department`.
- Data-cleaning functions are available as reusable module functions but are not yet integrated into the CLI workflow.
- Outlier detection identifies potential outliers without modifying the original dataset.

## Future Improvements

- Support dynamic chart selection based on dataset columns.
- Add configurable data-cleaning options to the CLI.
- Support additional input formats such as Excel.
- Add interactive visualizations.
- Preserve historical analysis reports.
- Introduce a configurable analysis pipeline.

## Author

**Nasrin Soufi**

[GitHub](https://github.com/nasrinsoufi)

[Portfolio](https://www.nasrin-soufi.ir)


