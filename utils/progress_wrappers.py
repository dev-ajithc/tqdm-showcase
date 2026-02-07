"""
Reusable progress bar wrappers for common operations.

This module provides convenient wrapper functions that add progress
tracking to common operations.
"""

import os
import shutil
from typing import Any, Callable, Iterable, List, Optional

from tqdm import tqdm


def progress_map(
    func: Callable[[Any], Any],
    iterable: Iterable[Any],
    desc: str = "Processing",
    **tqdm_kwargs: Any
) -> List[Any]:
    """
    Apply function to iterable with progress tracking.

    Args:
        func: Function to apply to each item
        iterable: Iterable to process
        desc: Description for progress bar
        **tqdm_kwargs: Additional arguments for tqdm

    Returns:
        List of results
    """
    items = list(iterable)
    results = []

    for item in tqdm(items, desc=desc, **tqdm_kwargs):
        results.append(func(item))

    return results


def progress_filter(
    predicate: Callable[[Any], bool],
    iterable: Iterable[Any],
    desc: str = "Filtering",
    **tqdm_kwargs: Any
) -> List[Any]:
    """
    Filter iterable with progress tracking.

    Args:
        predicate: Function to test each item
        iterable: Iterable to filter
        desc: Description for progress bar
        **tqdm_kwargs: Additional arguments for tqdm

    Returns:
        List of filtered items
    """
    items = list(iterable)
    results = []

    for item in tqdm(items, desc=desc, **tqdm_kwargs):
        if predicate(item):
            results.append(item)

    return results


def progress_copy(
    src: str,
    dst: str,
    chunk_size: int = 1024 * 1024
) -> None:
    """
    Copy file with progress tracking.

    Args:
        src: Source file path
        dst: Destination file path
        chunk_size: Size of each chunk in bytes
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source file not found: {src}")

    file_size = os.path.getsize(src)

    with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
        with tqdm(
            total=file_size,
            unit='B',
            unit_scale=True,
            desc=f"Copying {os.path.basename(src)}"
        ) as pbar:
            while True:
                chunk = fsrc.read(chunk_size)
                if not chunk:
                    break
                fdst.write(chunk)
                pbar.update(len(chunk))


def progress_copytree(
    src: str,
    dst: str,
    symlinks: bool = False,
    ignore: Optional[Callable[[str, List[str]], List[str]]] = None
) -> None:
    """
    Copy directory tree with progress tracking.

    Args:
        src: Source directory
        dst: Destination directory
        symlinks: Follow symbolic links
        ignore: Function to filter files to ignore
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory not found: {src}")

    file_list = []
    for root, dirs, files in os.walk(src):
        for file in files:
            file_list.append(os.path.join(root, file))

    os.makedirs(dst, exist_ok=True)

    for src_file in tqdm(file_list, desc="Copying files", unit="file"):
        rel_path = os.path.relpath(src_file, src)
        dst_file = os.path.join(dst, rel_path)

        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        shutil.copy2(src_file, dst_file)


def progress_reduce(
    func: Callable[[Any, Any], Any],
    iterable: Iterable[Any],
    initializer: Optional[Any] = None,
    desc: str = "Reducing",
    **tqdm_kwargs: Any
) -> Any:
    """
    Reduce iterable with progress tracking.

    Args:
        func: Binary function to apply
        iterable: Iterable to reduce
        initializer: Initial value
        desc: Description for progress bar
        **tqdm_kwargs: Additional arguments for tqdm

    Returns:
        Reduced result
    """
    items = list(iterable)

    if initializer is None:
        if not items:
            raise TypeError("reduce() of empty sequence")
        result = items[0]
        items = items[1:]
    else:
        result = initializer

    for item in tqdm(items, desc=desc, **tqdm_kwargs):
        result = func(result, item)

    return result


def progress_enumerate(
    iterable: Iterable[Any],
    start: int = 0,
    desc: str = "Processing",
    **tqdm_kwargs: Any
) -> List[tuple]:
    """
    Enumerate iterable with progress tracking.

    Args:
        iterable: Iterable to enumerate
        start: Starting index
        desc: Description for progress bar
        **tqdm_kwargs: Additional arguments for tqdm

    Returns:
        List of (index, item) tuples
    """
    items = list(iterable)
    results = []

    for idx, item in enumerate(
        tqdm(items, desc=desc, **tqdm_kwargs),
        start=start
    ):
        results.append((idx, item))

    return results


def progress_zip(
    *iterables: Iterable[Any],
    desc: str = "Zipping",
    **tqdm_kwargs: Any
) -> List[tuple]:
    """
    Zip iterables with progress tracking.

    Args:
        *iterables: Iterables to zip together
        desc: Description for progress bar
        **tqdm_kwargs: Additional arguments for tqdm

    Returns:
        List of tuples
    """
    lists = [list(it) for it in iterables]
    min_length = min(len(lst) for lst in lists)

    results = []
    for i in tqdm(range(min_length), desc=desc, **tqdm_kwargs):
        results.append(tuple(lst[i] for lst in lists))

    return results


class ProgressContext:
    """Context manager for progress tracking."""

    def __init__(
        self,
        total: int,
        desc: str = "Progress",
        **tqdm_kwargs: Any
    ) -> None:
        """
        Initialize progress context.

        Args:
            total: Total number of steps
            desc: Description for progress bar
            **tqdm_kwargs: Additional arguments for tqdm
        """
        self.pbar = tqdm(total=total, desc=desc, **tqdm_kwargs)

    def __enter__(self) -> 'ProgressContext':
        """Enter context."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Exit context and close progress bar."""
        self.pbar.close()

    def update(self, n: int = 1) -> None:
        """
        Update progress.

        Args:
            n: Number of steps to increment
        """
        self.pbar.update(n)

    def set_description(self, desc: str) -> None:
        """
        Set progress bar description.

        Args:
            desc: New description
        """
        self.pbar.set_description(desc)

    def set_postfix(self, **kwargs: Any) -> None:
        """
        Set progress bar postfix.

        Args:
            **kwargs: Key-value pairs for postfix
        """
        self.pbar.set_postfix(**kwargs)
