# Pytest Setup and Usage Guide

## Installing Pytest

### Option 1: Using pip (Recommended for this project)
```powershell
# Make sure virtual environment is activated
& .venv\Scripts\Activate.ps1

# Install pytest
pip install pytest --no-user

# Or install from requirements.txt
pip install -r requirements.txt --no-user
```

### Option 2: Using Poe the Poet

1. **Install poethepoet:**
```powershell
pip install poethepoet --no-user
```

2. **Create/Update `pyproject.toml`:**
```toml
[tool.poe.tasks]
install-dev = "pip install pytest pytest-cov pytest-asyncio"
test = "pytest"
test-verbose = "pytest -v"
test-coverage = "pytest --cov=. --cov-report=html"
```

3. **Run tasks:**
```powershell
poe install-dev  # Install pytest and related packages
poe test         # Run tests
```

### Option 3: Using Poetry

1. **Install Poetry:**
```powershell
pip install poetry --no-user
```

2. **Add pytest as dev dependency:**
```powershell
poetry add --group dev pytest
```

3. **Run tests:**
```powershell
poetry run pytest
```

## Running Tests

### Basic Commands
```powershell
# Run all tests
pytest

# Or use Python module syntax (if pytest not in PATH)
python -m pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test/test_example.py

# Run specific test function
pytest test/test_example.py::test_function_name

# Run with coverage
pytest --cov=. --cov-report=html
```

### Useful Pytest Options
```powershell
pytest -v              # Verbose output
pytest -s              # Show print statements
pytest -x              # Stop after first failure
pytest --lf            # Run last failed tests
pytest --ff            # Run failures first, then others
pytest -k "pattern"    # Run tests matching pattern
pytest --markers       # Show available markers
pytest --collect-only  # Show what tests would run
```

## Common Issues and Solutions

### Issue: "pytest: The term 'pytest' is not recognized"
**Solution:** Use `python -m pytest` instead, or ensure virtual environment is activated.

### Issue: "No module named pytest"
**Solution:** Install pytest in your virtual environment:
```powershell
pip install pytest --no-user
```

### Issue: Corporate proxy/Nexus blocking packages
**Solution:** Use `--no-user` flag and ensure you're using the Nexus repository:
```powershell
pip install pytest --no-user
```

## Project Structure for Tests
```
todos_backend/
├── test/
│   ├── __init__.py
│   ├── test_example.py
│   └── test_*.py         # All test files
├── main.py
├── models.py
├── requirements.txt
└── pytest.ini            # Optional pytest configuration
```

## Creating a pytest.ini Configuration (Optional)
Create `pytest.ini` in project root:
```ini
[pytest]
testpaths = test
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --strict-markers
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
```

## Example Test File
```python
# test/test_example.py
import pytest

def test_example():
    assert 1 + 1 == 2

def test_string():
    assert "hello".upper() == "HELLO"

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiply_by_two(input, expected):
    assert input * 2 == expected
```

## Additional Testing Packages
```powershell
# Install additional testing tools
pip install pytest-cov      # Coverage reporting
pip install pytest-asyncio  # Async test support
pip install pytest-mock     # Mocking utilities
pip install httpx          # For testing FastAPI endpoints
```

## Measuring Test Coverage with Pytest

### Install pytest-cov
```powershell
pip install pytest-cov --no-user
```

### Run Tests with Coverage

**Basic coverage report:**
```powershell
# Show coverage in terminal
pytest --cov=.

# Or specify specific directories/modules
pytest --cov=todos_backend --cov=routers
```

**Generate HTML coverage report:**
```powershell
pytest --cov=. --cov-report=html

# Then open htmlcov/index.html in your browser
```

**Show missing lines in terminal:**
```powershell
pytest --cov=. --cov-report=term-missing
```

**Combine multiple report formats:**
```powershell
pytest --cov=. --cov-report=html --cov-report=term-missing
```

### Understanding Coverage Output

**Terminal output example:**
```
---------- coverage: platform win32, python 3.13.9-final-0 -----------
Name                     Stmts   Miss  Cover   Missing
--------------------------------------------------------
main.py                     45     23    49%   12-18, 25-30, 45
models.py                   20     10    50%   5-8, 15-20
routers/auth.py             30     15    50%   10-15, 22-28
routers/todos.py            35     10    71%   40-45, 50-52
--------------------------------------------------------
TOTAL                      130     58    55%
```

**Columns explained:**
- **Stmts**: Total statements in the file
- **Miss**: Number of statements not covered by tests
- **Cover**: Coverage percentage (indicates how much is tested)
- **Missing**: Line numbers not covered by tests

**50% coverage means:**
- Half of your code statements are executed during tests
- The other half is untested

### Set Minimum Coverage Requirements

**Fail tests if coverage is below threshold:**
```powershell
# Fail if coverage is below 50%
pytest --cov=. --cov-fail-under=50

# Fail if coverage is below 80%
pytest --cov=. --cov-fail-under=80
```

### Coverage Configuration File

Create `.coveragerc` or add to `pyproject.toml`:

**Option 1: .coveragerc file**
```ini
[run]
source = .
omit = 
    */tests/*
    */test/*
    */__pycache__/*
    */venv/*
    */.venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:

[html]
directory = htmlcov
```

**Option 2: pyproject.toml**
```toml
[tool.coverage.run]
source = ["."]
omit = [
    "*/tests/*",
    "*/test/*",
    "*/__pycache__/*",
    "*/venv/*",
    "*/.venv/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]

[tool.coverage.html]
directory = "htmlcov"
```

### Viewing HTML Coverage Report

1. **Generate the report:**
```powershell
pytest --cov=. --cov-report=html
```

2. **Open the report:**
```powershell
# Windows
start htmlcov/index.html

# Or navigate to htmlcov/index.html in your browser
```

3. **What you'll see:**
   - Overall coverage percentage
   - List of all files with their coverage
   - Click on any file to see:
     - **Green lines**: Covered by tests
     - **Red lines**: Not covered by tests
     - **Yellow lines**: Partially covered (branches)

### Coverage Best Practices

**Good coverage targets:**
- **50-60%**: Minimum acceptable for legacy code
- **70-80%**: Good coverage for most projects
- **80-90%**: Excellent coverage
- **90%+**: Comprehensive coverage (may have diminishing returns)

**Focus on:**
- Critical business logic
- Error handling paths
- Edge cases
- Integration points

**Don't obsess over:**
- 100% coverage (rarely practical)
- Covering simple getters/setters
- Framework boilerplate code

### Common Coverage Commands Cheat Sheet

```powershell
# Quick coverage check
pytest --cov

# Detailed coverage with missing lines
pytest --cov=. --cov-report=term-missing

# HTML report for detailed analysis
pytest --cov=. --cov-report=html

# Coverage for specific module only
pytest --cov=routers tests/

# Coverage with minimum threshold
pytest --cov=. --cov-fail-under=70

# Multiple reports at once
pytest --cov=. --cov-report=html --cov-report=term --cov-report=xml

# Run specific tests with coverage
pytest tests/test_auth.py --cov=routers.auth
```

### Improving Coverage

**To reach 50% or higher coverage:**

1. **Identify uncovered code:**
```powershell
pytest --cov=. --cov-report=term-missing
```

2. **Look at the "Missing" column** - these are line numbers without tests

3. **Write tests for uncovered lines:**
```python
# If lines 12-18 in main.py are uncovered, add tests like:
def test_uncovered_function():
    result = uncovered_function()
    assert result == expected_value
```

4. **Re-run coverage to verify improvement:**
```powershell
pytest --cov=. --cov-report=term-missing
```

## FastAPI Testing Example
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```
