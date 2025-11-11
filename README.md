# E-Commerce Selenium Testing

![Tests](https://github.com/adammajcher86-hub/ecommerce-selenium-testing/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

> Automated web testing for e-commerce applications using Selenium WebDriver, Python, and Page Object Model.

## 🚀 Features

- Page Object Model design pattern
- Comprehensive test coverage (6 login tests)
- Screenshot on failure
- Detailed logging
- Cross-browser support
- CI/CD with GitHub Actions
- Headless mode for fast execution

## 🧪 Running Tests
```bash
# Run all tests (visible browser)
pytest -v tests/

# Run in headless mode (faster)
pytest -v tests/ --headless

# Run smoke tests only
pytest -v -m smoke tests/

# Run with HTML report
pytest -v --html=reports/report.html tests/
```

## 📊 CI/CD

Tests run automatically on:
- Every push to main/master
- Every pull request
- Python 3.10, 3.11, 3.12

Code quality checks:
- Black (code formatting)
- Ruff (linting)

## 📄 License

MIT License