"""
Base Page Object Model
Contains common methods used by all page objects
"""

import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.config import EXPLICIT_WAIT

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    def find_element(self, locator):
        """Find element with explicit wait"""
        try:
            logger.debug(f"Finding element: {locator}")
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise

    def find_elements(self, locator):
        """Find multiple elements with explicit wait"""
        try:
            logger.debug(f"Finding elements: {locator}")
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            logger.error(f"Elements not found: {locator}")
            raise

    def click(self, locator):
        """Click element with explicit wait for clickability"""
        try:
            logger.debug(f"Clicking element: {locator}")
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException:
            logger.error(f"Element not clickable: {locator}")
            raise

    def send_keys(self, locator, text):
        """Send keys to element with clear first"""
        try:
            logger.debug(f"Sending keys to element: {locator}")
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            logger.error(f"Failed to send keys to {locator}: {e}")
            raise

    def get_text(self, locator):
        """Get text from element"""
        try:
            element = self.find_element(locator)
            return element.text
        except Exception as e:
            logger.error(f"Failed to locate element {locator}: {e}")
            return False

    def is_visible(self, locator, timeout=EXPLICIT_WAIT):
        """Check if element is visible"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception as e:
            logger.error(f"Element is not visible {locator}: {e}")
            return False

    def is_present(self, locator, timeout=EXPLICIT_WAIT):
        """Check if element is present in DOM"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except Exception as e:
            logger.error(f"Element is not present in DOM {locator}: {e}")
            return False

    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url

    def get_title(self):
        """Get page title"""
        return self.driver.title

    def refresh_page(self):
        """Refresh the current page"""
        logger.info("Refreshing page")
        self.driver.refresh()

    def scroll_to_element(self, locator):
        """Scroll element into view"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.debug(f"Scrolled to element: {locator}")
