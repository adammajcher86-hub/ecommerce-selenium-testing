# E-Commerce Selenium Testing

![Tests](https://github.com/adammajcher86-hub/ecommerce-selenium-testing/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

> Automated web testing for e-commerce applications using Selenium WebDriver, Python, and Page Object Model.

## 🚀 Features

- Page Object Model design pattern
- Comprehensive test coverage (6 login tests and 6 products tests)
- Screenshot on failure
- Detailed logging
- Cross-browser support
- CI/CD with GitHub Actions
- Headless mode for fast execution
- Report available in every execution

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

#Run separate tests
pytest -v -s -k "test_sort_products_by_price_low_to_high or test_sort_products_by_name_z_to_a" --log-cli-level=DEBUG --headless
```

🔍 Debugging with Logs
```
Tests include detailed logging. View logs during test execution:

# Standard logging
pytest -v --log-cli-level=INFO tests/

# Detailed debugging
pytest -v --log-cli-level=DEBUG tests/

# Save logs to file
pytest -v --log-file=test_run.log tests/
```

Log levels:

    INFO - Test progress and results ✅
    WARNING - Retry attempts and fallbacks ⚠️
    DEBUG - Detailed request/response data 🔍
    ERROR - Critical failures ❌

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
