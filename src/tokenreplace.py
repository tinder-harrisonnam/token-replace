import os
import re
import sys
import json
import csv

def load_config(config_file_path):
    """
    Loads the configuration from a JSON file.
    Parameters:
    - config_file_path: The path to the JSON configuration file.
    Returns:
    A dictionary containing the configuration.
    """
    print("Loading configuration from:", config_file_path)
    with open(config_file_path, 'r', encoding='utf-8') as configfile:
        config = json.load(configfile)
    return config

def load_mappings_from_csv(csv_file_path):
    """
    Loads the hex to design system token mapping from a CSV file.
    Parameters:
    - csv_file_path: The path to the CSV file containing the mappings.
    Returns:
    A dictionary with hex color codes as keys and design system tokens as values.
    """
    print("Loading color mapping from CSV:", csv_file_path)
    color_mapping = {}
    with open(csv_file_path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            hex_color, token = row
            color_mapping[hex_color.upper()] = token
            print(f"Mapping added: {hex_color} -> {token}")
    return color_mapping

def combine_mappings(config_mappings, csv_mappings):
    """
    Combines mappings from the config and CSV file, with CSV taking precedence.
    Parameters:
    - config_mappings: Mappings from the config file.
    - csv_mappings: Mappings from the CSV file.
    Returns:
    A combined dictionary of mappings.
    """
    combined = config_mappings.copy()
    combined.update(csv_mappings)  # CSV mappings take precedence over config mappings
    return combined

def replace_values_in_file(file_path, mappings):
    """
    Replaces specified values in a file with corresponding design system tokens.
    Parameters:
    - file_path: The path to the file where replacements should be made.
    - mappings: A dictionary mapping values to design system tokens.
    """
    print("Processing file:", file_path)
    try:
        with open(file_path, 'r+') as file:
            content = file.read()
            original_content = content

            for value, token in mappings.items():
                pattern = re.compile(re.escape(value), re.IGNORECASE)
                content = pattern.sub(token, content)

            if content != original_content:
                file.seek(0)
                file.write(content)
                file.truncate()
                print("File updated successfully.")
            else:
                print("No changes made to the file.")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_directory(folder_path, mappings, file_extensions):
    """
    Processes each file in a specified directory, applying value replacements.
    Parameters:
    - folder_path: The path to the directory containing files to process.
    - mappings: A dictionary of values and their corresponding design system tokens.
    - file_extensions: A list of file extensions to process.
    """
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if any(file_name.endswith(ext) for ext in file_extensions):
                replace_values_in_file(os.path.join(root, file_name), mappings)

def process_file_or_directory(path, mappings, file_extensions):
    """
    Determines whether the given path is a file or directory and processes it accordingly.
    Parameters:
    - path: The path to either a single file or a directory of files.
    - mappings: A dictionary of values and their corresponding design system tokens.
    - file_extensions: A list of file extensions to process.
    """
    if os.path.isdir(path):
        print(f"Processing directory: {path}")
        process_directory(path, mappings, file_extensions)
    elif os.path.isfile(path) and any(path.endswith(ext) for ext in file_extensions):
        print(f"Processing single file: {path}")
        replace_values_in_file(path, mappings)
    else:
        print("The path provided does not exist or is not a valid file or directory.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python tokenreplace.py <path_to_config>")
        sys.exit(1)

    config_file_path = sys.argv[1]
    config = load_config(config_file_path)

    config_mappings = config.get("mappings", {})
    csv_file_path = config.get("csv_file_path")

    if csv_file_path:
        csv_mappings = load_mappings_from_csv(csv_file_path)
        mappings = combine_mappings(config_mappings, csv_mappings)
    else:
        mappings = config_mappings

    targets = config.get("targets", [])
    if not targets:
        print("No targets specified in the configuration file.")
        sys.exit(1)

    for target in targets:
        process_file_or_directory(
            path=target,
            mappings=mappings,
            file_extensions=config["file_extensions"]
        )

    print("Completed processing.")

if __name__ == "__main__":
    main()
