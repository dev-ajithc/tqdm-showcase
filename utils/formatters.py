"""
Custom formatters for TQDM progress bars.

This module provides custom formatting functions and styles
for progress bars.
"""

from typing import Any, Dict, Optional

from tqdm import tqdm


def bytes_formatter(n: float, pos: Optional[int] = None) -> str:
    """
    Format bytes into human-readable format.

    Args:
        n: Number of bytes
        pos: Position parameter (unused)

    Returns:
        Formatted string
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_idx = 0

    while n >= 1024 and unit_idx < len(units) - 1:
        n /= 1024
        unit_idx += 1

    return f"{n:.2f} {units[unit_idx]}"


def percentage_formatter(n: float, total: float) -> str:
    """
    Format progress as percentage.

    Args:
        n: Current progress
        total: Total steps

    Returns:
        Formatted percentage string
    """
    if total == 0:
        return "0.00%"
    percentage = (n / total) * 100
    return f"{percentage:.2f}%"


def time_formatter(seconds: float) -> str:
    """
    Format time duration into human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def create_custom_bar_format(
    show_percentage: bool = True,
    show_count: bool = True,
    show_rate: bool = True,
    show_elapsed: bool = True,
    show_remaining: bool = True
) -> str:
    """
    Create a custom bar format string.

    Args:
        show_percentage: Include percentage
        show_count: Include current/total count
        show_rate: Include processing rate
        show_elapsed: Include elapsed time
        show_remaining: Include remaining time

    Returns:
        Custom format string
    """
    parts = ["{desc}"]

    if show_percentage:
        parts.append("{percentage:3.0f}%")

    parts.append("{bar}")

    if show_count:
        parts.append("{n_fmt}/{total_fmt}")

    if show_rate:
        parts.append("{rate_fmt}")

    time_parts = []
    if show_elapsed:
        time_parts.append("{elapsed}")
    if show_remaining:
        time_parts.append("{remaining}")

    if time_parts:
        parts.append("[" + "<".join(time_parts) + "]")

    return ": ".join(parts[:2]) + " | " + " ".join(parts[2:])


class ColoredProgressBar(tqdm):
    """Progress bar with colored output based on progress."""

    COLORS = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'reset': '\033[0m'
    }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize colored progress bar."""
        super().__init__(*args, **kwargs)

    def format_meter(
        self,
        n: float,
        total: float,
        elapsed: float,
        ncols: Optional[int] = None,
        prefix: str = '',
        ascii: bool = False,
        unit: str = 'it',
        unit_scale: bool = False,
        rate: Optional[float] = None,
        bar_format: Optional[str] = None,
        postfix: Optional[str] = None,
        unit_divisor: int = 1000,
        **extra_kwargs: Any
    ) -> str:
        """Format meter with color based on progress percentage."""
        meter = super().format_meter(
            n, total, elapsed, ncols, prefix, ascii,
            unit, unit_scale, rate, bar_format,
            postfix, unit_divisor, **extra_kwargs
        )

        if total > 0:
            progress = n / total
            if progress < 0.33:
                color = self.COLORS['red']
            elif progress < 0.66:
                color = self.COLORS['yellow']
            else:
                color = self.COLORS['green']

            return f"{color}{meter}{self.COLORS['reset']}"

        return meter


class StyledProgressBar(tqdm):
    """Progress bar with custom styling options."""

    def __init__(
        self,
        *args: Any,
        style: str = 'default',
        **kwargs: Any
    ) -> None:
        """
        Initialize styled progress bar.

        Args:
            *args: Positional arguments for tqdm
            style: Style preset ('default', 'minimal', 'detailed')
            **kwargs: Keyword arguments for tqdm
        """
        if style == 'minimal':
            kwargs['bar_format'] = '{desc}: {percentage:3.0f}%|{bar}|'
        elif style == 'detailed':
            kwargs['bar_format'] = (
                '{desc}: {percentage:3.0f}%|{bar}| '
                '{n_fmt}/{total_fmt} '
                '[{elapsed}<{remaining}, {rate_fmt}]'
            )

        super().__init__(*args, **kwargs)


def create_metrics_display(metrics: Dict[str, Any]) -> str:
    """
    Create a formatted string for displaying metrics.

    Args:
        metrics: Dictionary of metric names and values

    Returns:
        Formatted metrics string
    """
    parts = []
    for key, value in metrics.items():
        if isinstance(value, float):
            parts.append(f"{key}={value:.4f}")
        else:
            parts.append(f"{key}={value}")

    return ", ".join(parts)


def progress_bar_with_metrics(
    iterable: Any,
    desc: str = "Processing",
    **kwargs: Any
) -> tqdm:
    """
    Create a progress bar configured for displaying metrics.

    Args:
        iterable: Iterable to track
        desc: Description for progress bar
        **kwargs: Additional tqdm arguments

    Returns:
        Configured tqdm instance
    """
    return tqdm(
        iterable,
        desc=desc,
        bar_format=(
            '{desc}: {percentage:3.0f}%|{bar}| '
            '{n_fmt}/{total_fmt} [{elapsed}<{remaining}] {postfix}'
        ),
        **kwargs
    )
