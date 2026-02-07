# TQDM Showcase: Progress Bars That Make You Feel Like a Hacker 🚀

> There's something satisfying about seeing a progress bar slide across
> the screen. With tqdm, even the most boring loop feels cinematic.

A comprehensive collection of TQDM examples, utilities, and best
practices for adding professional progress bars to your Python projects.

## 🎯 Why This Project?

I first added tqdm into a file-copying script just for fun. Then I
couldn't stop. Every long-running process in my scripts now has a sleek
progress bar. It's addictive because it gives instant feedback, and
trust me - once you add it, you'll never go back to blind loops.

## ✨ Features

- **Basic Examples**: Simple, fundamental tqdm usage patterns
- **File Operations**: Progress tracking for copying, moving files
- **Data Processing**: CSV, JSON processing with progress bars
- **Advanced Examples**: Threading, pandas integration, async operations
- **Download Tracking**: Monitor file downloads with progress
- **Reusable Utilities**: Drop-in wrapper functions
- **Custom Formatters**: Styled and colored progress bars
- **Full Test Coverage**: Unit tests for all utilities

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/yourusername/tqdm-showcase.git
cd tqdm-showcase
pip install -r requirements.txt
```

### Your First Progress Bar

```python
from tqdm import tqdm
import time

for i in tqdm(range(100)):
    time.sleep(0.05)
```

That's it! You now feel like a hacker. 😎

## 📚 Examples

### Basic Usage

Run the basic examples to see fundamental tqdm features:

```bash
python examples/basic_examples.py
```

Features demonstrated:
- Simple loop progress bars
- Custom descriptions
- Manual progress updates
- Nested progress bars
- Custom formatting
- Postfix information display

### File Operations

See progress bars in action with real file operations:

```bash
python examples/file_operations.py
```

Includes:
- File copying with progress
- Large file chunked copying
- Directory scanning
- Batch file operations

### Data Processing

Process data files with visual feedback:

```bash
python examples/data_processing.py
```

Demonstrates:
- CSV file processing
- JSON array handling
- Batch processing
- Data transformation
- Filtering and aggregation

### Advanced Features

Explore advanced use cases:

```bash
python examples/advanced_examples.py
```

Features:
- Multi-threaded processing
- Pandas DataFrame operations
- Pandas groupby with progress
- Multiple concurrent progress bars
- Custom progress bar classes

### Download Examples

Track downloads and API requests:

```bash
python examples/download_examples.py
```

## 🛠️ Utilities

### Progress Wrappers

Convenient wrapper functions for common operations:

```python
from utils.progress_wrappers import progress_map, progress_filter

# Map with progress
results = progress_map(lambda x: x * 2, data, desc="Processing")

# Filter with progress
filtered = progress_filter(lambda x: x > 0, data, desc="Filtering")

# Copy file with progress
from utils.progress_wrappers import progress_copy
progress_copy('source.txt', 'destination.txt')
```

### Custom Formatters

Create styled progress bars:

```python
from utils.formatters import StyledProgressBar, ColoredProgressBar

# Styled progress bar
for item in StyledProgressBar(data, style='detailed'):
    process(item)

# Colored progress bar (changes color based on progress)
for item in ColoredProgressBar(data, desc="Processing"):
    process(item)
```

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=. --cov-report=term-missing
```

Run code quality checks:

```bash
flake8 .
```

## 📖 Documentation

Additional documentation is available in the `docs/` directory:

- `getting_started.md` - Beginner's guide to tqdm
- `use_cases.md` - Common use cases and patterns
- `best_practices.md` - Tips and best practices

## 🎨 Project Structure

```
tqdm-showcase/
├── examples/           # Example scripts
│   ├── basic_examples.py
│   ├── file_operations.py
│   ├── data_processing.py
│   ├── advanced_examples.py
│   └── download_examples.py
├── utils/             # Reusable utilities
│   ├── progress_wrappers.py
│   └── formatters.py
├── tests/             # Unit tests
│   ├── test_progress_wrappers.py
│   └── test_formatters.py
├── docs/              # Documentation
├── requirements.txt   # Dependencies
├── setup.cfg          # Configuration
└── README.md
```

## 💡 Common Use Cases

### Processing Large Files

```python
from tqdm import tqdm

with open('large_file.txt', 'r') as f:
    lines = f.readlines()

for line in tqdm(lines, desc="Processing lines"):
    process(line)
```

### API Requests with Rate Limiting

```python
from tqdm import tqdm
import time

for item in tqdm(items, desc="API requests", unit="req"):
    response = api_call(item)
    time.sleep(0.5)  # Rate limiting
```

### Pandas DataFrame Operations

```python
import pandas as pd
from tqdm import tqdm

tqdm.pandas(desc="Processing rows")
df['result'] = df['column'].progress_apply(lambda x: process(x))
```

### Multi-threaded Processing

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(process, item) for item in items]

    for future in tqdm(as_completed(futures), total=len(items)):
        result = future.result()
```

## 🔧 Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Code Quality

This project maintains high code quality standards:

- PEP 8 compliance (79 character line length)
- Type hints for all functions
- Comprehensive docstrings
- Unit tests with >80% coverage
- Security best practices
- No flake8 violations

## 🔒 Security

This project follows security best practices:

- Secure package versions
- Input validation
- Safe file operations
- Environment variable usage
- Proper error handling

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [tqdm](https://github.com/tqdm/tqdm) - The amazing progress bar
library
- The Python community for continuous inspiration

## 📬 Contact

Questions? Suggestions? Open an issue or reach out!

---

**Made with ❤️ and lots of progress bars**
