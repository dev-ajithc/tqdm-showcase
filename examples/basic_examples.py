"""
Basic TQDM examples demonstrating fundamental usage patterns.

This module showcases the most common and essential tqdm use cases.
"""

import time
from typing import List

from tqdm import tqdm


def simple_loop() -> None:
    """
    The classic tqdm example - a simple progress bar for a loop.

    This is the example that makes you feel like a hacker!
    """
    print("\n1. Simple Loop Progress Bar")
    print("-" * 50)

    for i in tqdm(range(100), desc="Processing"):
        time.sleep(0.05)


def custom_description() -> None:
    """Demonstrate custom descriptions and dynamic updates."""
    print("\n2. Custom Description Progress Bar")
    print("-" * 50)

    for i in tqdm(range(50), desc="Loading data", unit="items"):
        time.sleep(0.03)


def manual_progress() -> None:
    """Manually update progress bar with custom increments."""
    print("\n3. Manual Progress Updates")
    print("-" * 50)

    with tqdm(total=100, desc="Manual control") as pbar:
        for i in range(10):
            time.sleep(0.1)
            pbar.update(10)


def nested_progress_bars() -> None:
    """Show nested progress bars for hierarchical operations."""
    print("\n4. Nested Progress Bars")
    print("-" * 50)

    for i in tqdm(range(5), desc="Outer loop", position=0):
        for j in tqdm(range(20), desc="Inner loop", position=1,
                      leave=False):
            time.sleep(0.02)


def custom_format() -> None:
    """Custom format string for progress bar display."""
    print("\n5. Custom Format")
    print("-" * 50)

    bar_format = (
        "{desc}: {percentage:3.0f}%|{bar}| "
        "{n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
    )

    for i in tqdm(range(75), desc="Custom format",
                  bar_format=bar_format):
        time.sleep(0.03)


def progress_with_postfix() -> None:
    """Show additional information using postfix."""
    print("\n6. Progress Bar with Postfix Info")
    print("-" * 50)

    pbar = tqdm(range(50), desc="Training")
    for i in pbar:
        loss = 1.0 / (i + 1)
        accuracy = (i + 1) / 50.0
        pbar.set_postfix(
            loss=f"{loss:.4f}",
            acc=f"{accuracy:.2%}"
        )
        time.sleep(0.05)


def iterable_wrapping() -> None:
    """Wrap any iterable with tqdm."""
    print("\n7. Wrapping Iterables")
    print("-" * 50)

    data: List[str] = [f"item_{i}" for i in range(30)]

    for item in tqdm(data, desc="Processing items"):
        time.sleep(0.05)


def progress_with_rate() -> None:
    """Display processing rate in the progress bar."""
    print("\n8. Progress Bar with Rate Display")
    print("-" * 50)

    for i in tqdm(range(100), desc="Processing", unit="items",
                  unit_scale=True):
        time.sleep(0.02)


def main() -> None:
    """Run all basic examples."""
    print("=" * 50)
    print("TQDM Basic Examples - Feel Like a Hacker!")
    print("=" * 50)

    simple_loop()
    custom_description()
    manual_progress()
    nested_progress_bars()
    custom_format()
    progress_with_postfix()
    iterable_wrapping()
    progress_with_rate()

    print("\n" + "=" * 50)
    print("All basic examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
