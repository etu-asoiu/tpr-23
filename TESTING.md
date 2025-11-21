# Testing Documentation

## Overview

This project has comprehensive test coverage for the optimization module extracted from the TPR.ipynb notebook. We have achieved **100% code coverage** with both statement and branch coverage.

## Test Structure

```
tests/
  __init__.py
  test_optimization.py    # 54 comprehensive tests
src/
  __init__.py
  optimization.py         # Main optimization module
```

## Running Tests

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage Report

```bash
pytest --cov=src --cov-report=term-missing
```

### Generate HTML Coverage Report

```bash
pytest --cov=src --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

## Test Coverage

### Current Coverage: 100%

- **Statements**: 47/47 (100%)
- **Branches**: 12/12 (100%)
- **Total**: 100%

### Coverage Breakdown

| Module | Statements | Missing | Branches | Partial | Coverage |
|--------|-----------|---------|----------|---------|----------|
| src/__init__.py | 0 | 0 | 0 | 0 | 100% |
| src/optimization.py | 47 | 0 | 12 | 0 | 100% |
| **TOTAL** | **47** | **0** | **12** | **0** | **100%** |

## Test Organization

### 1. Basic Functions Tests (26 tests)
- `TestIncomeFunction1`: Tests for workshop 1 income calculation
- `TestIncomeFunction2`: Tests for workshop 2 income calculation
- `TestRemainderFunction1`: Tests for workshop 1 remainder calculation
- `TestRemainderFunction2`: Tests for workshop 2 remainder calculation
- `TestTotalRevenueF`: Tests for workshop 1 total revenue
- `TestTotalRevenueG`: Tests for workshop 2 total revenue
- `TestGoalFunction`: Tests for the optimization goal function

### 2. Optimization Functions Tests (13 tests)
- `TestOptimizeBruteForce`: Tests for brute force optimization
  - Different investment amounts
  - Different step sizes
  - Edge cases
- `TestOptimizeScipy`: Tests for scipy-based optimization
  - Different investment amounts
  - Custom initial guesses
  - Edge cases

### 3. Simulation Tests (15 tests)
- `TestSimulateQuarters`: Tests for multi-quarter simulation
  - Both scipy and brute force methods
  - Different numbers of quarters
  - Method comparison
  - Edge cases

## Test Features

### Edge Cases Covered
- Zero investment
- Very small investments
- Large investments
- Fractional investments
- Different optimization methods
- Invalid method names

### Validation Tests
- Function correctness
- Return types
- Boundary conditions
- Mathematical properties
- Algorithm comparison

## Configuration Files

### pytest.ini
Configures pytest to:
- Run tests in the `tests/` directory
- Generate coverage reports
- Require 100% coverage
- Show missing lines

### .coveragerc
Configures coverage.py to:
- Track branch coverage
- Generate HTML and XML reports
- Exclude test files from coverage

## Continuous Integration

To add CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=src --cov-report=xml

- name: Check coverage
  run: |
    coverage report --fail-under=100
```

## Adding New Tests

When adding new functionality to `src/optimization.py`:

1. Add corresponding tests to `tests/test_optimization.py`
2. Run tests: `pytest`
3. Check coverage: `pytest --cov=src --cov-report=term-missing`
4. Ensure 100% coverage is maintained

## Notes

- All tests pass successfully (54/54)
- No missing coverage
- Both statement and branch coverage at 100%
- Tests include edge cases and validation
