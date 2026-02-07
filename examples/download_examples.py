"""
Download examples with TQDM progress bars.

This module demonstrates file downloads with progress tracking.
"""

import os
import time
from typing import Optional
from urllib.parse import urlparse

import requests
from tqdm import tqdm


def download_file_with_progress(
    url: str,
    destination: Optional[str] = None,
    chunk_size: int = 8192
) -> Optional[str]:
    """
    Download a file with progress bar.

    Args:
        url: URL to download from
        destination: Local file path (auto-generated if None)
        chunk_size: Size of chunks to download

    Returns:
        Path to downloaded file, or None if failed
    """
    print(f"\nDownloading: {url}")
    print("-" * 50)

    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        if destination is None:
            parsed = urlparse(url)
            destination = os.path.basename(parsed.path) or "download"

        total_size = int(response.headers.get('content-length', 0))

        with open(destination, 'wb') as f, tqdm(
            desc=os.path.basename(destination),
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

        print(f"Downloaded to: {destination}")
        return destination

    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")
        return None


def download_multiple_files(
    urls: list,
    destination_dir: str = "downloads"
) -> list:
    """
    Download multiple files with progress tracking.

    Args:
        urls: List of URLs to download
        destination_dir: Directory to save files

    Returns:
        List of downloaded file paths
    """
    print(f"\nDownloading {len(urls)} files")
    print("-" * 50)

    os.makedirs(destination_dir, exist_ok=True)

    downloaded_files = []

    for url in tqdm(urls, desc="Overall progress", unit="file"):
        parsed = urlparse(url)
        filename = (
            os.path.basename(parsed.path)
            or f"file_{len(downloaded_files)}"
        )
        destination = os.path.join(destination_dir, filename)

        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))

            with open(destination, 'wb') as f:
                with tqdm(
                    desc=f"  {filename}",
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    leave=False
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

            downloaded_files.append(destination)

        except requests.exceptions.RequestException as e:
            print(f"  Failed to download {url}: {e}")

    return downloaded_files


def simulate_api_requests(count: int = 20) -> list:
    """
    Simulate API requests with rate limiting and progress.

    Args:
        count: Number of requests to make

    Returns:
        List of responses
    """
    print(f"\nSimulating {count} API Requests")
    print("-" * 50)

    responses = []

    for i in tqdm(range(count), desc="API requests", unit="req"):
        time.sleep(0.2)
        responses.append({'id': i, 'status': 'success'})

    return responses


def main() -> None:
    """Run download examples."""
    print("=" * 50)
    print("TQDM Download Examples")
    print("=" * 50)

    simulate_api_requests(15)

    print("\n" + "=" * 50)
    print("Download examples completed!")
    print("=" * 50)
    print("\nNote: Actual file downloads are commented out")
    print("to avoid external dependencies in demo.")


if __name__ == "__main__":
    main()
