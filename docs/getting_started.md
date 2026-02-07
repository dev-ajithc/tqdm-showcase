# Getting Started with TQDM

## What is TQDM?

TQDM is a fast, extensible progress bar library for Python. The name
comes from the Arabic word "taqaddum" (تقدّم) which means "progress".

## Installation

```bash
pip install tqdm
```

## Your First Progress Bar

The simplest way to use tqdm is to wrap any iterable:

```python
from tqdm import tqdm
import time

for i in tqdm(range(100)):
    time.sleep(0.01)
```

## Basic Concepts

### 1. Wrapping Iterables

TQDM works by wrapping any iterable:

```python
from tqdm import tqdm

# Lists
for item in tqdm([1, 2, 3, 4, 5]):
    process(item)

# Ranges
for i in tqdm(range(1000)):
    process(i)

# Files
with open('file.txt', 'r') as f:
    for line in tqdm(f):
        process(line)
```

### 2. Custom Descriptions

Add meaningful descriptions to your progress bars:

```python
for i in tqdm(range(100), desc="Processing items"):
    process(i)
```

### 3. Manual Updates

For more control, use manual updates:

```python
from tqdm import tqdm

with tqdm(total=100) as pbar:
    for i in range(10):
        # Do work
        process_batch()
        # Update progress
        pbar.update(10)
```

### 4. Nested Progress Bars

Track multiple levels of progress:

```python
from tqdm import tqdm

for i in tqdm(range(10), desc="Outer"):
    for j in tqdm(range(20), desc="Inner", leave=False):
        process(i, j)
```

## Common Parameters

### Essential Parameters

- `total`: Total number of iterations (auto-detected for iterables)
- `desc`: Description prefix
- `disable`: Disable the progress bar (useful for production)
- `unit`: Unit of iteration (default: 'it')
- `unit_scale`: Auto-scale large numbers

### Display Parameters

- `ncols`: Width of the progress bar
- `bar_format`: Custom format string
- `leave`: Keep the bar after completion (default: True)
- `position`: Position for nested bars

### Example with Common Parameters

```python
from tqdm import tqdm

for i in tqdm(range(1000),
              desc="Processing",
              unit="items",
              unit_scale=True,
              ncols=80):
    process(i)
```

## Best Practices

### 1. Use Descriptive Text

```python
# Good
for file in tqdm(files, desc="Processing images"):
    process(file)

# Better
for file in tqdm(files, desc="Converting images to PNG"):
    process(file)
```

### 2. Add Units

```python
# Generic
for item in tqdm(items):
    process(item)

# Better
for item in tqdm(items, unit="file"):
    process(item)
```

### 3. Show Additional Info

```python
pbar = tqdm(range(100))
for i in pbar:
    loss = calculate_loss()
    pbar.set_postfix(loss=f"{loss:.4f}")
```

### 4. Handle Errors Gracefully

```python
from tqdm import tqdm

pbar = tqdm(items)
try:
    for item in pbar:
        process(item)
finally:
    pbar.close()
```

Or use context managers:

```python
with tqdm(items) as pbar:
    for item in pbar:
        process(item)
```

## Next Steps

- Explore file operations in `file_operations.py`
- Learn data processing patterns in `data_processing.py`
- Check advanced features in `advanced_examples.py`
- Review utility functions in `utils/`

## Tips

1. **Performance**: TQDM is fast, but for very tight loops,
   consider using `mininterval` to reduce update frequency
2. **Logging**: Use `tqdm.write()` instead of `print()` to avoid
   interfering with the progress bar
3. **Jupyter**: TQDM works great in Jupyter notebooks with
   `from tqdm.notebook import tqdm`
4. **Silent Mode**: Use `disable=True` to turn off progress bars
   in production or CI/CD environments
