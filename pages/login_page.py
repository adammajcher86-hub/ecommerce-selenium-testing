"""
Login Page Object Model
Represents the SauceDemo login page
"""

import logging
from selenium.webdriver.common.by import By
from pages.page_base import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Page Object for SauceDemo login page"""

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_BUTTON = (By.CSS_SELECTOR, ".error-button")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/"

    def open(self):
        """Navigate to login page"""
        logger.info(f"Opening login page: {self.url}")
        self.driver.get(self.url)

    def enter_username(self, username):
        """Enter username in username field"""
        logger.info(f"Entering username: {username}")
        self.send_keys(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        """Enter password in password field"""
        logger.info("Entering password")
        self.send_keys(self.PASSWORD_INPUT, password)

    def click_login_button(self):
        """Click the login button"""
        logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        """Complete login flow"""
        logger.info(f"Attempting login with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def get_error_message(self):
        """Get error message text"""
        if self.is_visible(self.ERROR_MESSAGE, timeout=3):
            error_text = self.get_text(self.ERROR_MESSAGE)
            logger.info(f"Error message displayed: {error_text}")
            return error_text
        return None

    def is_error_displayed(self):
        """Check if error message is displayed"""
        return self.is_visible(self.ERROR_MESSAGE, timeout=3)

    def clear_error(self):
        """Click the error button to clear error message"""
        if self.is_visible(self.ERROR_BUTTON, timeout=2):
            logger.info("Clearing error message")
            self.click(self.ERROR_BUTTON)
