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

## Test Files

### test_utils.py (47 tests, 83% coverage)
Tests for utility functions in `src/utils.py`:

- **TestParseInstructionsImpl**: Tests for the pure `_parse_instructions_impl()` function
  - Empty/None input handling
  - Single and multiline strings
  - List processing with whitespace stripping
  - Type conversions

- **TestParseInstructions**: Tests for `parse_instructions()` with logging
  - Basic functionality
  - Error handling and edge cases
  - Content preservation

- **TestCleanUnitStringImpl**: Tests for the pure `_clean_unit_string_impl()` function
  - Unit object representation parsing (e.g., "Unit('cup')")
  - Plain string handling
  - Quote and whitespace stripping
  - Complex unit names

- **TestCleanUnitString**: Tests for `clean_unit_string()` with logging
  - Basic functionality
  - None handling
  - Content preservation across conversions

### test_ingredients.py (19 tests, 82% coverage)
Tests for ingredient parsing in `src/ingredients.py`:

- **TestNormalizeIngredientImpl**: Tests for pure `_normalize_ingredient_impl()` function
  - Dict-like parsed ingredients with quantity/unit/name extraction
  - Object-like parsed ingredients with attributes
  - Fallback to original ingredient string
  - Various field names (amount, size, name, ingredient, parsed)
  - Type conversions for quantities

- **TestNormalizeIngredient**: Tests for `normalize_ingredient()` with parsing
  - Successful parsing workflows
  - Error handling and fallbacks
  - Special character handling in ingredients

- **TestParseIngredients**: Tests for `parse_ingredients()` batch processing
  - Empty list handling
  - Multiple ingredients processing
  - Type conversions (quantity, unit, name)
  - Error handling per ingredient

### test_scraper.py (12 tests, 87% coverage)
Tests for recipe scraping in `src/scraper.py`:

- **TestScrapeRecipeFromUrl**: Tests for `scrape_recipe_from_url()` main scraping function
  - Successful recipe scraping with all fields
  - Scraper initialization error handling
  - Missing/unavailable fields (graceful degradation)
  - Title/ingredient/instruction extraction errors
  - Time value conversion to strings
  - Zero/falsy value handling

- **TestGetSupportedSites**: Tests for `get_supported_sites()` function
  - Returns list of supported sites
  - Sites are sorted
  - Error handling

- **TestScrapingError**: Tests for the ScrapingError exception
  - Exception creation
  - Raising and catching

### test_api.py (20 tests, 100% coverage)
Tests for Flask API endpoints in `src/api.py`:

- **TestHealthCheck**: Health check endpoint tests
  - Returns 200 status with healthy message
  - Returns valid JSON

- **TestScrapeEndpoint**: Main scraping endpoint tests (`POST /scrape`)
  - Valid URL scraping
  - JSON body validation
  - URL validation (required, not empty, has protocol)
  - HTTP/HTTPS protocol support
  - ScrapingError handling
  - Unexpected error handling
  - Complete recipe data return

- **TestSupportedSitesEndpoint**: Supported sites endpoint tests (`GET /supported-sites`)
  - Returns list of supported sites
  - Handles empty site list
  - Returns valid JSON

- **TestErrorHandlers**: Flask error handler tests
  - 404 Not Found handling
  - 405 Method Not Allowed handling

- **TestInvalidURLError**: Custom exception tests
  - Exception creation and inheritance

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

## Test Design Principles

### Testability Refactoring

The codebase was refactored to improve testability:

1. **Pure Functions**: Core logic extracted into pure functions (prefix with `_impl`)
   - `_parse_instructions_impl()` - No side effects, no logging
   - `_clean_unit_string_impl()` - No side effects, no logging
   - `_normalize_ingredient_impl()` - No side effects, accepts unit_cleaner callback

2. **Separation of Concerns**:
   - Pure logic functions are easy to unit test
   - Wrapper functions add logging and error handling
   - Dependencies are injectable (e.g., unit_cleaner parameter)

3. **Mocking Strategy**:
   - External dependencies (recipe_scrapers, ingredient_parser) are mocked
   - Flask app is configured in test mode
   - Test client provided via pytest fixtures

## Coverage Report

Current test coverage:

```
Name                 Stmts   Miss  Cover
------------------------------------------
src/__init__.py          0      0   100%
src/api.py              50      0   100%
src/ingredients.py      96     17    82%
src/scraper.py          70      9    87%
src/utils.py            35      6    83%
------------------------------------------
TOTAL                  251     32    87%
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
