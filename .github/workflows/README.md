# GitHub Actions

This project uses GitHub Actions for continuous integration and code quality checks.

## Workflows

### CI Workflow (`.github/workflows/ci.yml`)

Runs on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**

1. **Pre-commit Checks** (runs first):
   - Runs pre-commit hooks on all files
   - Ensures code quality and formatting standards
   - Caches pre-commit dependencies for faster runs
   - Must pass before tests can run

2. **Test Matrix** (runs after pre-commit passes):
   - Tests on Python 3.10, 3.11, 3.12, and 3.13
   - Runs full test suite with verbose output and coverage
   - Uploads coverage to Codecov (Python 3.11 only)
   - Uses `-v --cov-report=term-missing` for detailed test output

### Pre-commit Configuration

The CI runs pre-commit hooks (without pytest-check):
- **Ruff**: Linting and formatting
- **isort**: Import sorting
- **Pre-commit hooks**: Basic file validation
- **Bandit**: Security scanning

Tests are run separately with more verbosity for better debugging.

## Usage

### Local Development

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### CI/CD

The workflows automatically:
1. **Validate** code quality on every push/PR
2. **Test** across multiple Python versions
3. **Report** coverage metrics
4. **Ensure** consistent code formatting

### Status Badges

Add these badges to your README:

```markdown
![CI](https://github.com/yourusername/wifiqr/workflows/CI/badge.svg)
![codecov](https://codecov.io/gh/yourusername/wifiqr/branch/main/graph/badge.svg)
```
