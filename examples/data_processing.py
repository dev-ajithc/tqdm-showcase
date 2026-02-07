"""
Data processing examples with TQDM progress bars.

This module demonstrates processing CSV, JSON, and other data formats
with progress tracking.
"""

import csv
import json
import os
import time
from typing import Any, Dict, List

from tqdm import tqdm


def process_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Read and process a CSV file with progress tracking.

    Args:
        file_path: Path to CSV file

    Returns:
        List of processed records
    """
    print("\nProcessing CSV File")
    print("-" * 50)

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    with open(file_path, 'r') as f:
        total_lines = sum(1 for _ in f) - 1

    processed_data: List[Dict[str, Any]] = []

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in tqdm(
            reader,
            total=total_lines,
            desc="Processing CSV"
        ):
            processed_data.append(row)
            time.sleep(0.01)

    return processed_data


def process_json_array(file_path: str) -> List[Dict[str, Any]]:
    """
    Process a JSON array file with progress tracking.

    Args:
        file_path: Path to JSON file

    Returns:
        List of processed records
    """
    print("\nProcessing JSON Array")
    print("-" * 50)

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    with open(file_path, 'r') as f:
        data = json.load(f)

    processed_data: List[Dict[str, Any]] = []

    for item in tqdm(data, desc="Processing JSON"):
        processed_data.append(item)
        time.sleep(0.01)

    return processed_data


def batch_process_data(
    data: List[Any],
    batch_size: int = 10
) -> List[List[Any]]:
    """
    Process data in batches with progress tracking.

    Args:
        data: List of data items
        batch_size: Size of each batch

    Returns:
        List of processed batches
    """
    print(f"\nBatch Processing (batch_size={batch_size})")
    print("-" * 50)

    batches: List[List[Any]] = []
    total_batches = (len(data) + batch_size - 1) // batch_size

    for i in tqdm(range(0, len(data), batch_size),
                  total=total_batches,
                  desc="Processing batches",
                  unit="batch"):
        batch = data[i:i + batch_size]
        batches.append(batch)
        time.sleep(0.05)

    return batches


def transform_data_with_progress(
    data: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Transform data records with progress tracking.

    Args:
        data: List of data records

    Returns:
        List of transformed records
    """
    print("\nTransforming Data")
    print("-" * 50)

    transformed: List[Dict[str, Any]] = []

    for record in tqdm(data, desc="Transforming records"):
        transformed_record = {
            k.upper(): v for k, v in record.items()
        }
        transformed.append(transformed_record)
        time.sleep(0.01)

    return transformed


def filter_data_with_progress(
    data: List[Dict[str, Any]],
    key: str,
    value: Any
) -> List[Dict[str, Any]]:
    """
    Filter data with progress tracking.

    Args:
        data: List of data records
        key: Key to filter on
        value: Value to match

    Returns:
        List of filtered records
    """
    print(f"\nFiltering Data (key={key}, value={value})")
    print("-" * 50)

    filtered: List[Dict[str, Any]] = []

    for record in tqdm(data, desc="Filtering records"):
        if record.get(key) == value:
            filtered.append(record)
        time.sleep(0.005)

    print(f"Filtered: {len(filtered)}/{len(data)} records")
    return filtered


def create_sample_csv(file_path: str, rows: int = 100) -> None:
    """
    Create a sample CSV file for demonstration.

    Args:
        file_path: Path for the CSV file
        rows: Number of rows to create
    """
    print(f"\nCreating Sample CSV ({rows} rows)")
    print("-" * 50)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'age', 'city'])

        for i in tqdm(range(rows), desc="Writing CSV rows"):
            writer.writerow([
                i,
                f"Person_{i}",
                20 + (i % 50),
                f"City_{i % 10}"
            ])


def create_sample_json(file_path: str, count: int = 100) -> None:
    """
    Create a sample JSON file for demonstration.

    Args:
        file_path: Path for the JSON file
        count: Number of records to create
    """
    print(f"\nCreating Sample JSON ({count} records)")
    print("-" * 50)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    data: List[Dict[str, Any]] = []

    for i in tqdm(range(count), desc="Creating JSON records"):
        data.append({
            'id': i,
            'name': f"User_{i}",
            'email': f"user{i}@example.com",
            'score': (i * 7) % 100
        })

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def aggregate_data_with_progress(
    data: List[Dict[str, Any]],
    group_key: str
) -> Dict[str, int]:
    """
    Aggregate data by key with progress tracking.

    Args:
        data: List of data records
        group_key: Key to group by

    Returns:
        Dictionary with aggregated counts
    """
    print(f"\nAggregating Data by '{group_key}'")
    print("-" * 50)

    aggregated: Dict[str, int] = {}

    for record in tqdm(data, desc="Aggregating"):
        key_value = str(record.get(group_key, 'unknown'))
        aggregated[key_value] = aggregated.get(key_value, 0) + 1
        time.sleep(0.005)

    return aggregated


def main() -> None:
    """Run data processing examples."""
    print("=" * 50)
    print("TQDM Data Processing Examples")
    print("=" * 50)

    os.makedirs("sample_data", exist_ok=True)

    csv_file = "sample_data/sample.csv"
    json_file = "sample_data/sample.json"

    create_sample_csv(csv_file, 50)
    create_sample_json(json_file, 50)

    csv_data = process_csv_file(csv_file)
    process_json_array(json_file)

    batch_process_data(csv_data, batch_size=10)

    transform_data_with_progress(csv_data[:20])

    filter_data_with_progress(
        csv_data,
        'city',
        'City_0'
    )

    aggregated = aggregate_data_with_progress(csv_data, 'city')
    print(f"\nAggregation results: {aggregated}")

    import shutil
    if os.path.exists("sample_data"):
        shutil.rmtree("sample_data")

    print("\n" + "=" * 50)
    print("Data processing examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
