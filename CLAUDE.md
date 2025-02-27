# Adaptive Cards Toolkit Guide

## Build/Test Commands
- Install package: `pip install -e .`
- Run all tests: `python tests/run_tests.py`
- Single test: `python -m pytest tests/path/to/test_file.py::TestClass::test_method -v`
- Lint code: `black . && isort . && flake8 && mypy src/`
- Build package: `python -m build`

## Style Guidelines
- **Formatting**: Black with 88 character line length 
- **Imports**: Use isort with black profile (grouped by stdlib, third-party, local)
- **Types**: Full type hints required (mypy with disallow_untyped_defs=true)
- **Naming**: snake_case for methods/variables, PascalCase for classes
- **Error handling**: Use custom exceptions from utils.exceptions
- **Package structure**: Code should live in src/adaptive_cards_toolkit/