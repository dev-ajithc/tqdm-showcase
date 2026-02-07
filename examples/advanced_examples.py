"""
Advanced TQDM examples with threading, async, and pandas integration.

This module demonstrates complex use cases and advanced features.
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, List

import pandas as pd
from tqdm import tqdm


def multithreaded_processing(
    items: List[Any],
    worker_func: Callable[[Any], Any],
    max_workers: int = 4
) -> List[Any]:
    """
    Process items using multiple threads with progress tracking.

    Args:
        items: List of items to process
        worker_func: Function to apply to each item
        max_workers: Maximum number of worker threads

    Returns:
        List of processed results
    """
    print(f"\nMultithreaded Processing ({max_workers} workers)")
    print("-" * 50)

    results: List[Any] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(worker_func, item): item
            for item in items
        }

        for future in tqdm(
            as_completed(futures),
            total=len(items),
            desc="Processing items"
        ):
            results.append(future.result())

    return results


def sample_worker(item: Any) -> Any:
    """
    Sample worker function that simulates processing.

    Args:
        item: Item to process

    Returns:
        Processed result
    """
    time.sleep(0.1)
    return f"Processed: {item}"


def pandas_dataframe_operations() -> None:
    """Demonstrate tqdm integration with pandas operations."""
    print("\nPandas DataFrame Operations")
    print("-" * 50)

    data = {
        'id': range(100),
        'value': [i * 2 for i in range(100)],
        'category': [f"Cat_{i % 5}" for i in range(100)]
    }

    df = pd.DataFrame(data)

    tqdm.pandas(desc="Applying function")

    df['processed'] = df['value'].progress_apply(
        lambda x: x ** 2 if x % 2 == 0 else x * 3
    )

    print(f"\nDataFrame shape: {df.shape}")
    print(f"Sample data:\n{df.head()}")


def pandas_groupby_with_progress() -> None:
    """Show progress for pandas groupby operations."""
    print("\nPandas GroupBy with Progress")
    print("-" * 50)

    data = {
        'category': [f"Cat_{i % 5}" for i in range(200)],
        'value': list(range(200)),
        'score': [(i * 7) % 100 for i in range(200)]
    }

    df = pd.DataFrame(data)

    tqdm.pandas(desc="Grouping and aggregating")

    result = df.groupby('category').progress_apply(
        lambda x: x['value'].sum()
    )

    print(f"\nGroupBy results:\n{result}")


def pandas_iteration_with_progress() -> None:
    """Iterate through DataFrame rows with progress."""
    print("\nPandas Row Iteration with Progress")
    print("-" * 50)

    data = {
        'name': [f"User_{i}" for i in range(50)],
        'age': [20 + (i % 40) for i in range(50)],
        'score': [i * 2 for i in range(50)]
    }

    df = pd.DataFrame(data)

    processed_rows: List[str] = []

    for _, row in tqdm(df.iterrows(),
                       total=len(df),
                       desc="Processing rows"):
        processed = (
            f"{row['name']}: "
            f"age={row['age']}, "
            f"score={row['score']}"
        )
        processed_rows.append(processed)
        time.sleep(0.02)

    print(f"\nProcessed {len(processed_rows)} rows")


def multiple_concurrent_progress_bars() -> None:
    """Display multiple progress bars simultaneously."""
    print("\nMultiple Concurrent Progress Bars")
    print("-" * 50)

    def worker_task(task_id: int, items: int) -> None:
        """Simulate a task with its own progress bar."""
        for _ in tqdm(
            range(items),
            desc=f"Task {task_id}",
            position=task_id,
            leave=True
        ):
            time.sleep(0.05)

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(worker_task, i, 20)
            for i in range(3)
        ]

        for future in futures:
            future.result()


def progress_with_callback() -> None:
    """Use tqdm with callback functions."""
    print("\nProgress Bar with Callbacks")
    print("-" * 50)

    def process_item(item: int, pbar: tqdm) -> int:
        """Process an item and update progress."""
        time.sleep(0.05)
        pbar.update(1)
        return item * 2

    with tqdm(total=50, desc="Processing with callback") as pbar:
        results = [process_item(i, pbar) for i in range(50)]

    print(f"Processed {len(results)} items")


def custom_progress_bar_class() -> None:
    """Create a custom progress bar with special formatting."""
    print("\nCustom Progress Bar Class")
    print("-" * 50)

    class CustomProgressBar(tqdm):
        """Custom progress bar with additional features."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Initialize custom progress bar."""
            super().__init__(*args, **kwargs)
            self.errors = 0
            self.warnings = 0

        def add_error(self) -> None:
            """Increment error count."""
            self.errors += 1
            self.set_postfix(errors=self.errors, warnings=self.warnings)

        def add_warning(self) -> None:
            """Increment warning count."""
            self.warnings += 1
            self.set_postfix(errors=self.errors, warnings=self.warnings)

    pbar = CustomProgressBar(range(100), desc="Custom processing")
    for i in pbar:
        if i % 10 == 0:
            pbar.add_error()
        elif i % 5 == 0:
            pbar.add_warning()
        time.sleep(0.03)


def rate_limited_progress() -> None:
    """Demonstrate progress bar with rate limiting."""
    print("\nRate Limited Progress")
    print("-" * 50)

    items_per_second = 10
    delay = 1.0 / items_per_second

    for i in tqdm(range(50),
                  desc="Rate limited",
                  unit="req"):
        time.sleep(delay)


def main() -> None:
    """Run all advanced examples."""
    print("=" * 50)
    print("TQDM Advanced Examples")
    print("=" * 50)

    items = [f"item_{i}" for i in range(20)]
    multithreaded_processing(items, sample_worker, max_workers=4)

    pandas_dataframe_operations()
    pandas_groupby_with_progress()
    pandas_iteration_with_progress()

    multiple_concurrent_progress_bars()
    progress_with_callback()
    custom_progress_bar_class()
    rate_limited_progress()

    print("\n" + "=" * 50)
    print("Advanced examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
