"""
Login Tests for SauceDemo
"""

import pytest
import logging
from pages.login_page import LoginPage
from config.config import STANDARD_USER, LOCKED_OUT_USER

logger = logging.getLogger(__name__)


class TestLogin:
    """Test suite for login functionality"""

    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_with_valid_credentials(self, driver):
        """Test successful login with valid credentials"""
        logger.info("Testing login with valid credentials")

        login_page = LoginPage(driver)
        login_page.open()

        login_page.login(
            username=STANDARD_USER["username"], password=STANDARD_USER["password"]
        )

        assert (
            "inventory.html" in driver.current_url
        ), "Should be redirected to products page after login"

        logger.info("✅ Login successful - redirected to products page")

    @pytest.mark.negative
    @pytest.mark.login
    def test_login_with_invalid_username(self, driver):
        """Test login fails with invalid username"""
        logger.info("Testing login with invalid username")

        login_page = LoginPage(driver)
        login_page.open()

        login_page.login(username="invalid_user", password="secret_sauce")

        assert login_page.is_error_displayed(), "Error message should be displayed"

        error_message = login_page.get_error_message()
        assert (
            "Username and password do not match" in error_message
        ), "Should show authentication error"

        logger.info(f"✅ Login failed as expected with error: {error_message}")

    @pytest.mark.negative
    @pytest.mark.login
    def test_login_with_invalid_password(self, driver):
        """Test login fails with invalid password"""
        logger.info("Testing login with invalid password")

        login_page = LoginPage(driver)
        login_page.open()

        login_page.login(username=STANDARD_USER["username"], password="wrong_password")

        assert login_page.is_error_displayed(), "Error message should be displayed"

        error_message = login_page.get_error_message()
        assert (
            "Username and password do not match" in error_message
        ), "Should show authentication error"

        logger.info(f"✅ Login failed as expected with error: {error_message}")

    @pytest.mark.negative
    @pytest.mark.login
    def test_login_with_empty_credentials(self, driver):
        """Test login fails with empty username and password"""
        logger.info("Testing login with empty credentials")

        login_page = LoginPage(driver)
        login_page.open()

        login_page.click_login_button()

        assert login_page.is_error_displayed(), "Error message should be displayed"

        error_message = login_page.get_error_message()
        assert (
            "Username is required" in error_message
        ), "Should show username required error"

        logger.info(f"✅ Login failed as expected with error: {error_message}")

    @pytest.mark.negative
    @pytest.mark.login
    def test_login_with_locked_out_user(self, driver):
        """Test login fails for locked out user"""
        logger.info("Testing login with locked out user")

        login_page = LoginPage(driver)
        login_page.open()

        login_page.login(
            username=LOCKED_OUT_USER["username"], password=LOCKED_OUT_USER["password"]
        )

        assert login_page.is_error_displayed(), "Error message should be displayed"

        error_message = login_page.get_error_message()
        assert (
            "Sorry, this user has been locked out" in error_message
        ), "Should show locked out error"

        logger.info(f"✅ Login failed as expected with error: {error_message}")

    @pytest.mark.login
    def test_error_message_can_be_closed(self, driver):
        """Test that error message can be dismissed"""
        logger.info("Testing error message dismissal")

        login_page = LoginPage(driver)
        login_page.open()

        login_page.login(username="invalid", password="invalid")
        assert login_page.is_error_displayed(), "Error should be displayed"

        login_page.clear_error()

        assert not login_page.is_error_displayed(), "Error message should be dismissed"

        logger.info("✅ Error message successfully dismissed")
