# Contributing to Adaptive Cards Toolkit

Thank you for your interest in contributing to the Adaptive Cards Toolkit project! We welcome contributions from everyone, whether you're fixing a typo, adding new features, improving documentation, or reporting bugs.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```
   git clone https://github.com/your-username/adaptive-cards-toolkit.git
   cd adaptive-cards-toolkit
   ```
3. Install development dependencies:
   ```
   pip install -r requirements-dev.txt
   ```
4. Create a new branch for your changes:
   ```
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Before submitting a pull request, please run these tools:

```bash
# Format code with Black
black .

# Sort imports
isort .

# Run linting checks
flake8 .

# Run type checking
mypy .
```

### Testing

All new features and bug fixes should include tests. We use `pytest` for our test suite:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=term-missing
```

## Pull Request Process

1. Update the documentation if needed.
2. Make sure all tests pass.
3. Include a clear and descriptive commit message.
4. Push your changes to your fork and submit a pull request.
5. Wait for a maintainer to review your PR, make any requested changes, and get your PR merged.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We expect all contributors to adhere to the following principles:

- Be welcoming and inclusive
- Be respectful of different viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.