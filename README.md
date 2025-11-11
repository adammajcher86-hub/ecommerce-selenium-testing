# E-Commerce Selenium Testing

Automated web testing for e-commerce applications using Selenium WebDriver, Python, and Page Object Model.

## 🚀 Features

- Page Object Model design pattern
- Comprehensive test coverage
- Screenshot on failure
- Detailed logging
- Cross-browser support (Chrome, Firefox)
- CI/CD ready

## 🛠️ Tech Stack

- Python 3.9+
- Selenium WebDriver
- PyTest
- Page Object Model

## 📦 Installation
```bash
# Clone repository
git clone https://github.com/adammajcher86-hub/ecommerce-selenium-testing.git
cd ecommerce-selenium-testing

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🧪 Running Tests
```bash
# Run all tests
pytest -v tests/

# Run smoke tests only
pytest -v -m smoke tests/

# Run with HTML report
pytest -v --html=reports/report.html tests/
```

## 📊 Test Coverage

- Login functionality (6 tests)
- Product browsing (coming soon)
- Shopping cart (coming soon)
- Checkout flow (coming soon)

## 🎯 Target Application

Tests run against [SauceDemo](https://www.saucedemo.com/) - a demo e-commerce site.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.