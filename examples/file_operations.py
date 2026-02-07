"""
File operation examples with TQDM progress bars.

This module demonstrates real-world file handling scenarios with
progress tracking.
"""

import os
import shutil
import time
from typing import List

from tqdm import tqdm


def copy_files_with_progress(
    source_files: List[str],
    dest_dir: str
) -> None:
    """
    Copy multiple files with a progress bar.

    Args:
        source_files: List of source file paths
        dest_dir: Destination directory path
    """
    print("\nCopying Files with Progress")
    print("-" * 50)

    os.makedirs(dest_dir, exist_ok=True)

    for file_path in tqdm(source_files, desc="Copying files",
                          unit="file"):
        if os.path.exists(file_path):
            dest_path = os.path.join(
                dest_dir,
                os.path.basename(file_path)
            )
            shutil.copy2(file_path, dest_path)
        time.sleep(0.1)


def copy_large_file_with_progress(
    source: str,
    destination: str,
    chunk_size: int = 1024 * 1024
) -> None:
    """
    Copy a large file with chunk-based progress tracking.

    Args:
        source: Source file path
        destination: Destination file path
        chunk_size: Size of each chunk in bytes (default 1MB)
    """
    print("\nCopying Large File with Chunk Progress")
    print("-" * 50)

    if not os.path.exists(source):
        print(f"Source file not found: {source}")
        return

    file_size = os.path.getsize(source)

    with open(source, 'rb') as src, open(destination, 'wb') as dst:
        with tqdm(total=file_size, unit='B', unit_scale=True,
                  desc=f"Copying {os.path.basename(source)}") as pbar:
            while True:
                chunk = src.read(chunk_size)
                if not chunk:
                    break
                dst.write(chunk)
                pbar.update(len(chunk))


def scan_directory_with_progress(directory: str) -> List[str]:
    """
    Scan directory and count files with progress.

    Args:
        directory: Directory path to scan

    Returns:
        List of file paths found
    """
    print("\nScanning Directory")
    print("-" * 50)

    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return []

    all_files: List[str] = []

    for root, dirs, files in os.walk(directory):
        for file in tqdm(
            files,
            desc=f"Scanning {root}",
            leave=False
        ):
            all_files.append(os.path.join(root, file))
            time.sleep(0.01)

    print(f"Total files found: {len(all_files)}")
    return all_files


def move_files_with_progress(
    source_files: List[str],
    dest_dir: str
) -> None:
    """
    Move multiple files with progress tracking.

    Args:
        source_files: List of source file paths
        dest_dir: Destination directory path
    """
    print("\nMoving Files with Progress")
    print("-" * 50)

    os.makedirs(dest_dir, exist_ok=True)

    for file_path in tqdm(source_files, desc="Moving files",
                          unit="file"):
        if os.path.exists(file_path):
            dest_path = os.path.join(
                dest_dir,
                os.path.basename(file_path)
            )
            shutil.move(file_path, dest_path)
        time.sleep(0.1)


def create_sample_files(count: int = 10) -> List[str]:
    """
    Create sample files for demonstration.

    Args:
        count: Number of sample files to create

    Returns:
        List of created file paths
    """
    print("\nCreating Sample Files")
    print("-" * 50)

    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)

    file_paths: List[str] = []

    for i in tqdm(range(count), desc="Creating files"):
        file_path = os.path.join(temp_dir, f"sample_{i}.txt")
        with open(file_path, 'w') as f:
            f.write(f"Sample content for file {i}\n" * 100)
        file_paths.append(file_path)
        time.sleep(0.05)

    return file_paths


def delete_files_with_progress(file_paths: List[str]) -> None:
    """
    Delete multiple files with progress tracking.

    Args:
        file_paths: List of file paths to delete
    """
    print("\nDeleting Files with Progress")
    print("-" * 50)

    for file_path in tqdm(file_paths, desc="Deleting files",
                          unit="file"):
        if os.path.exists(file_path):
            os.remove(file_path)
        time.sleep(0.05)


def main() -> None:
    """Run file operation examples."""
    print("=" * 50)
    print("TQDM File Operations Examples")
    print("=" * 50)

    sample_files = create_sample_files(10)

    copy_files_with_progress(
        sample_files[:5],
        "temp_files/copied"
    )

    scan_directory_with_progress("temp_files")

    delete_files_with_progress(sample_files)

    if os.path.exists("temp_files"):
        shutil.rmtree("temp_files")

    print("\n" + "=" * 50)
    print("File operations examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
