# TQDM Best Practices

## Performance Optimization

### 1. Minimize Update Frequency

For very tight loops, reduce update frequency:

```python
from tqdm import tqdm

# Default: updates every iteration (can be slow)
for i in tqdm(range(1000000)):
    fast_operation(i)

# Better: update less frequently
for i in tqdm(range(1000000), mininterval=0.5):
    fast_operation(i)
```

### 2. Disable in Production

```python
import os
from tqdm import tqdm

# Disable in production or CI
disable_progress = os.getenv('CI') == 'true'

for item in tqdm(items, disable=disable_progress):
    process(item)
```

### 3. Use Context Managers

Always use context managers for proper cleanup:

```python
# Good
with tqdm(total=100) as pbar:
    for i in range(100):
        process(i)
        pbar.update(1)

# Or
for item in tqdm(items):
    process(item)
```

## Display Best Practices

### 1. Descriptive Labels

```python
# Poor
for i in tqdm(range(100)):
    process(i)

# Better
for i in tqdm(range(100), desc="Processing"):
    process(i)

# Best
for i in tqdm(range(100), desc="Converting images to PNG"):
    process(i)
```

### 2. Appropriate Units

```python
# Files
tqdm(files, unit="file")

# Bytes
tqdm(total=file_size, unit='B', unit_scale=True)

# Requests
tqdm(requests, unit="req")

# Custom
tqdm(items, unit="widget")
```

### 3. Show Progress Metrics

```python
from tqdm import tqdm

pbar = tqdm(range(100))
for i in pbar:
    accuracy = calculate_accuracy()
    loss = calculate_loss()

    pbar.set_postfix(
        acc=f"{accuracy:.2%}",
        loss=f"{loss:.4f}"
    )
```

## Error Handling

### 1. Always Clean Up

```python
from tqdm import tqdm

pbar = tqdm(items)
try:
    for item in pbar:
        process(item)
except Exception as e:
    pbar.set_description("Failed")
    raise
finally:
    pbar.close()
```

### 2. Graceful Degradation

```python
from tqdm import tqdm

try:
    progress = tqdm(items)
except Exception:
    progress = items  # Fallback to no progress

for item in progress:
    process(item)
```

## Logging Integration

### 1. Use tqdm.write()

```python
from tqdm import tqdm

for item in tqdm(items):
    result = process(item)
    if result.error:
        tqdm.write(f"Error processing {item}: {result.error}")
```

### 2. Redirect stdout

```python
from tqdm import tqdm
import sys

with tqdm(total=100, file=sys.stdout) as pbar:
    for i in range(100):
        process(i)
        pbar.update(1)
```

## Nested Progress Bars

### 1. Use position Parameter

```python
from tqdm import tqdm

for i in tqdm(range(5), desc="Outer", position=0):
    for j in tqdm(range(20), desc="Inner", position=1, leave=False):
        process(i, j)
```

### 2. Clean Up Inner Bars

```python
from tqdm import tqdm

for category in tqdm(categories, desc="Categories"):
    for item in tqdm(items, desc=f"  {category}", leave=False):
        process(category, item)
```

## Multi-threading

### 1. One Progress Bar per Thread

```python
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def worker(item, position):
    for _ in tqdm(range(10), desc=f"Worker {position}",
                 position=position):
        process(item)

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(worker, item, i)
        for i, item in enumerate(items)
    ]
```

### 2. Single Shared Progress Bar

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def worker(item):
    return process(item)

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(worker, item): item for item in items}

    for future in tqdm(as_completed(futures), total=len(items)):
        result = future.result()
```

## Custom Formatting

### 1. Create Reusable Formats

```python
from tqdm import tqdm

DETAILED_FORMAT = (
    '{desc}: {percentage:3.0f}%|{bar}| '
    '{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
)

MINIMAL_FORMAT = '{desc}: {percentage:3.0f}%|{bar}|'

for item in tqdm(items, bar_format=DETAILED_FORMAT):
    process(item)
```

### 2. Dynamic Descriptions

```python
from tqdm import tqdm

pbar = tqdm(range(100))
for i in pbar:
    stage = "preprocessing" if i < 50 else "postprocessing"
    pbar.set_description(f"{stage.capitalize()}")
    process(i)
```

## Testing

### 1. Disable in Tests

```python
import pytest
from tqdm import tqdm

@pytest.fixture
def disable_tqdm():
    tqdm.__init__.__defaults__ = (None,) * len(
        tqdm.__init__.__defaults__[:-1]
    ) + (True,)

def test_with_progress(disable_tqdm):
    for item in tqdm(items):
        assert process(item) == expected
```

### 2. Mock Progress Bars

```python
from unittest.mock import patch
from tqdm import tqdm

def test_processing():
    with patch('tqdm.tqdm') as mock_tqdm:
        mock_tqdm.return_value.__iter__ = lambda x: iter(items)
        process_with_progress(items)
        mock_tqdm.assert_called_once()
```

## Memory Management

### 1. Don't Store All Items

```python
# Bad: Loads everything into memory
items = list(generate_large_dataset())
for item in tqdm(items):
    process(item)

# Good: Stream processing
for item in tqdm(generate_large_dataset()):
    process(item)
```

### 2. Close Progress Bars

```python
from tqdm import tqdm

# Automatic cleanup with context manager
with tqdm(total=100) as pbar:
    for i in range(100):
        pbar.update(1)

# Manual cleanup
pbar = tqdm(total=100)
try:
    for i in range(100):
        pbar.update(1)
finally:
    pbar.close()
```

## Jupyter Notebooks

### 1. Use Notebook Widget

```python
from tqdm.notebook import tqdm

for item in tqdm(items, desc="Processing"):
    process(item)
```

### 2. Auto Display

```python
from tqdm.auto import tqdm

# Automatically uses notebook widget in Jupyter
# and console version elsewhere
for item in tqdm(items):
    process(item)
```

## Common Pitfalls to Avoid

### 1. Don't Modify tqdm Objects from Multiple Threads

```python
# Bad: Race conditions
pbar = tqdm(total=100)
for item in items:
    thread_process(item, pbar)  # Multiple threads access pbar

# Good: Use locks or separate progress bars
```

### 2. Don't Forget Total for Generators

```python
# Bad: No progress percentage
for item in tqdm(generator()):
    process(item)

# Good: Provide total
total = count_items()
for item in tqdm(generator(), total=total):
    process(item)
```

### 3. Don't Mix print() and tqdm

```python
# Bad: Messes up display
for item in tqdm(items):
    print(f"Processing {item}")
    process(item)

# Good: Use tqdm.write()
for item in tqdm(items):
    tqdm.write(f"Processing {item}")
    process(item)
```

## Summary

1. **Always** use descriptive labels and appropriate units
2. **Always** clean up with context managers or try-finally
3. **Never** use print() - use tqdm.write() instead
4. **Consider** disabling in production/CI environments
5. **Optimize** update frequency for performance-critical code
6. **Show** relevant metrics with set_postfix()
7. **Test** with progress bars disabled or mocked
8. **Use** tqdm.auto for universal compatibility
