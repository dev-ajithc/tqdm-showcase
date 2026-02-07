"""
Tests for custom formatters.
"""

from utils.formatters import (
    bytes_formatter,
    create_custom_bar_format,
    create_metrics_display,
    percentage_formatter,
    time_formatter,
)


def test_bytes_formatter() -> None:
    """Test bytes formatter."""
    assert bytes_formatter(1024) == "1.00 KB"
    assert bytes_formatter(1024 * 1024) == "1.00 MB"
    assert bytes_formatter(1024 * 1024 * 1024) == "1.00 GB"
    assert bytes_formatter(500) == "500.00 B"


def test_percentage_formatter() -> None:
    """Test percentage formatter."""
    assert percentage_formatter(50, 100) == "50.00%"
    assert percentage_formatter(75, 100) == "75.00%"
    assert percentage_formatter(0, 100) == "0.00%"
    assert percentage_formatter(100, 100) == "100.00%"
    assert percentage_formatter(0, 0) == "0.00%"


def test_time_formatter() -> None:
    """Test time formatter."""
    assert time_formatter(30) == "30s"
    assert time_formatter(90) == "1m 30s"
    assert time_formatter(3665) == "1h 1m 5s"
    assert time_formatter(7200) == "2h 0m 0s"


def test_create_custom_bar_format() -> None:
    """Test custom bar format creation."""
    format_str = create_custom_bar_format()
    assert "{desc}" in format_str
    assert "{bar}" in format_str
    assert "{percentage" in format_str

    minimal_format = create_custom_bar_format(
        show_percentage=False,
        show_count=False,
        show_rate=False
    )
    assert "{desc}" in minimal_format
    assert "{bar}" in minimal_format


def test_create_metrics_display() -> None:
    """Test metrics display creation."""
    metrics = {
        'loss': 0.1234,
        'accuracy': 0.9567,
        'epoch': 5
    }

    display = create_metrics_display(metrics)

    assert 'loss=0.1234' in display
    assert 'accuracy=0.9567' in display
    assert 'epoch=5' in display


def test_create_metrics_display_empty() -> None:
    """Test metrics display with empty dict."""
    display = create_metrics_display({})
    assert display == ""
