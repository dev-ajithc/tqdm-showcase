"""
Tests for progress wrapper utilities.
"""

import os
import tempfile

import pytest

from utils.progress_wrappers import (
    ProgressContext,
    progress_copy,
    progress_enumerate,
    progress_filter,
    progress_map,
    progress_reduce,
    progress_zip,
)


def test_progress_map() -> None:
    """Test progress_map function."""
    data = [1, 2, 3, 4, 5]
    result = progress_map(lambda x: x * 2, data, desc="Testing map")

    assert result == [2, 4, 6, 8, 10]


def test_progress_filter() -> None:
    """Test progress_filter function."""
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = progress_filter(
        lambda x: x % 2 == 0,
        data,
        desc="Testing filter"
    )

    assert result == [2, 4, 6, 8, 10]


def test_progress_copy() -> None:
    """Test progress_copy function."""
    with tempfile.TemporaryDirectory() as tmpdir:
        src_file = os.path.join(tmpdir, "source.txt")
        dst_file = os.path.join(tmpdir, "destination.txt")

        with open(src_file, 'w') as f:
            f.write("Test content\n" * 1000)

        progress_copy(src_file, dst_file)

        assert os.path.exists(dst_file)
        with open(dst_file, 'r') as f:
            content = f.read()
        assert "Test content" in content


def test_progress_copy_file_not_found() -> None:
    """Test progress_copy with non-existent file."""
    with pytest.raises(FileNotFoundError):
        progress_copy("nonexistent.txt", "destination.txt")


def test_progress_reduce() -> None:
    """Test progress_reduce function."""
    data = [1, 2, 3, 4, 5]
    result = progress_reduce(
        lambda x, y: x + y,
        data,
        initializer=0,
        desc="Testing reduce"
    )

    assert result == 15


def test_progress_enumerate() -> None:
    """Test progress_enumerate function."""
    data = ['a', 'b', 'c']
    result = progress_enumerate(data, start=1, desc="Testing enum")

    assert result == [(1, 'a'), (2, 'b'), (3, 'c')]


def test_progress_zip() -> None:
    """Test progress_zip function."""
    list1 = [1, 2, 3]
    list2 = ['a', 'b', 'c']
    list3 = [10, 20, 30]

    result = progress_zip(list1, list2, list3, desc="Testing zip")

    assert result == [(1, 'a', 10), (2, 'b', 20), (3, 'c', 30)]


def test_progress_context() -> None:
    """Test ProgressContext context manager."""
    with ProgressContext(total=10, desc="Testing context") as ctx:
        for i in range(10):
            ctx.update(1)
            ctx.set_postfix(current=i)

    assert True


def test_progress_context_description_update() -> None:
    """Test updating description in ProgressContext."""
    with ProgressContext(total=5, desc="Initial") as ctx:
        for i in range(5):
            ctx.set_description(f"Step {i}")
            ctx.update(1)

    assert True
