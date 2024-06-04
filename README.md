# Token Replace Tool

### Overview

The Token Replace Tool is a Python script designed to replace specified values in files with design system tokens. It supports processing individual files and directories, with mappings provided either directly in the configuration file or in a CSV file.

### Features

- Replace values in various file types
- Support for mappings provided directly in the configuration file or through a CSV file.
- Process individual files or directories.

### Installation

#### Prerequisites

- Python 3.x
- `pip3` (Python package installer)

#### Steps

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd token-replace-tool
    ```

2. Install the package in editable mode:

    ```sh
    pip3 install -e .
    ```

### Usage

#### Running the Tool
You can run the tool using the defined entry point:
  ```sh
  tokenreplace config/test_config.json
  ```

This command processes the fiels specified in the `test_config.json` configuration file.

### Configuration
The configuration file should be in JSON format. Below is an example configuration file(`config/test_config.json`):

```json
{
    "targets": [
        "tests/test_data/test_file.xml",
        "tests/test_data/test_file.swift",
        "tests/test_data/test_file.html",
        "tests/test_data/test_file.tsx"
    ],
    "file_extensions": [".xml", ".swift", ".html", ".tsx"],
    "mappings": {
        "#F8F8F8": "@color/ds_color_gray_05",
        "#4A4A4A": "@color/ds_color_dark"
    },
    "csv_file_path": "config/example_mappings.csv"
}
```

#### Configuration paramters
- `targets`: List of files or directories to process
- `file_extensions`: List of file extensions to process
- `mappings`: Dictinoary of values to replace with their corresponding design token
- `csv_file_path`: Path to a CSV file containing additional mappings. If this is specified, the mappings from the CSV file will take precedence over those specified directly in the configuration file.
