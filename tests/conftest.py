"""
Pytest configuration and fixtures
"""

import pytest
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.config import (
    DEFAULT_BROWSER,
    IMPLICIT_WAIT,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    SCREENSHOT_ON_FAILURE,
    SCREENSHOT_DIR,
)

logger = logging.getLogger(__name__)


def get_chrome_options(headless=False):
    """Configure Chrome options"""
    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument("--headless=new")
        logger.info("Running Chrome in headless mode")

    # Basic arguments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")

    # Disable automation detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Disable notifications, popups, and password manager
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
    }
    options.add_experimental_option("prefs", prefs)

    return options


def get_firefox_options(headless=False):
    """Configure Firefox options"""
    options = webdriver.FirefoxOptions()

    if headless:
        options.add_argument("--headless")
        logger.info("Running Firefox in headless mode")

    return options


@pytest.fixture(scope="function")
def driver(request):
    """
    Setup and teardown for WebDriver
    Scope: function - new browser instance for each test
    """
    browser = request.config.getoption("--browser", default=DEFAULT_BROWSER)
    headless = request.config.getoption("--headless")

    logger.info(f"Initializing {browser} browser (headless={headless})")

    # Initialize driver based on browser choice
    if browser.lower() == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(
            service=service, options=get_chrome_options(headless=headless)
        )
    elif browser.lower() == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(
            service=service, options=get_firefox_options(headless=headless)
        )
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    # Configure driver
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)

    logger.info(f"Browser initialized: {browser}")

    yield driver

    # Teardown
    if SCREENSHOT_ON_FAILURE and request.node.rep_call.failed:
        take_screenshot(driver, request.node.nodeid)

    logger.info(f"Closing {browser} browser")
    driver.quit()


@pytest.fixture(scope="function", autouse=True)
def log_test_name(request):
    """Log test name before and after execution"""
    test_name = request.node.nodeid
    logger.info(f"{'=' * 80}")
    logger.info(f"STARTING TEST: {test_name}")
    logger.info(f"{'=' * 80}")

    yield

    logger.info(f"{'=' * 80}")
    logger.info(f"FINISHED TEST: {test_name}")
    logger.info(f"{'=' * 80}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Make test result available to fixtures
    Used for screenshot on failure
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def take_screenshot(driver, test_name):
    """Take screenshot and save to file"""
    try:
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_name = test_name.replace("::", "_").replace("/", "_")
        filename = f"{clean_name}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)

        driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved: {filepath}")

    except Exception as e:
        logger.error(f"Failed to take screenshot: {e}")


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser",
        action="store",
        default=DEFAULT_BROWSER,
        help="Browser to run tests on: chrome, firefox",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,  # ✅ Changed to False - browser visible by default
        help="Run browser in headless mode",
    )
