"""
# Testing Guide for Recipe Scraper API

## Overview

This test suite provides comprehensive unit tests for the Recipe Scraper API. The tests are organized by module and cover all major functionality with 87% code coverage.

## Test Structure

```
tests/
├── __init__.py          # Test package initialization
├── conftest.py          # Pytest configuration and fixtures
├── test_api.py          # Flask API endpoint tests
├── test_scraper.py      # Recipe scraping logic tests
├── test_ingredients.py  # Ingredient parsing tests
└── test_utils.py        # Utility function tests
```

## Running Tests

### Run all tests
```bash
pytest tests/
```

### Run with verbose output
```bash
pytest tests/ -v
```

### Run specific test file
```bash
pytest tests/test_utils.py -v
```

### Run specific test class
```bash
pytest tests/test_api.py::TestHealthCheck -v
```

### Run specific test
```bash
pytest tests/test_utils.py::TestParseInstructionsImpl::test_empty_string -v
```

### Run with coverage report
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Generate HTML coverage report
```bash
pytest tests/ --cov=src --cov-report=html
```

## Key Test Fixtures

From `tests/conftest.py`:

- **app**: Flask test application with TESTING=True
- **client**: Flask test client for making requests to endpoints

## Dependencies

Test dependencies are listed in `requirements.txt`:

- **pytest** (7.4.3) - Test framework
- **pytest-mock** (3.12.0) - Enhanced mocking support
- **pytest-cov** (4.1.0) - Coverage measurement

## Best Practices Used

1. **Descriptive Test Names**: Each test clearly describes what is being tested
2. **Docstrings**: Every test has a docstring explaining the test case
3. **Arrange-Act-Assert**: Clear test structure
4. **DRY Principle**: Fixtures and helper methods reduce duplication
5. **Mocking External Dependencies**: External APIs are mocked
6. **Edge Case Testing**: Empty inputs, None values, falsy values
7. **Error Scenarios**: Both success and failure paths tested
8. **Type Validation**: Ensures correct types are returned

## Extending Tests

When adding new tests:

1. Follow the existing class/module organization
2. Use descriptive test names with test_ prefix
3. Add docstrings to all test functions
4. Use mocks for external dependencies
5. Test both success and failure cases
6. Include edge cases (empty, None, boundary values)
7. Run coverage report to identify untested code

## Common Issues

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Python Path Issues
Tests use relative imports from the project root. Run tests from project directory:
```bash
cd /path/to/recipe-scraper-api
pytest tests/
```

### Module Not Found
Ensure `.venv` is activated and dependencies are installed:
```bash
python -m pip install -r requirements.txt
```

## Continuous Integration

To integrate tests into CI/CD:

```bash
# Run tests with coverage
pytest tests/ --cov=src --cov-report=xml

# Run tests with specific markers (if added in future)
pytest tests/ -m "unit"

# Run with JUnit XML output for CI systems
pytest tests/ --junit-xml=test-results.xml
```
