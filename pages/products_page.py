"""
Products Page Object Model
Represents the SauceDemo products/inventory page
"""

import logging

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from pages.page_base import BasePage
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


logger = logging.getLogger(__name__)


class ProductsPage(BasePage):
    """Page Object for SauceDemo products page"""

    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    SHOPPING_CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CHECKOUT_CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/inventory.html"

    def is_loaded(self):
        """Check if products page is loaded"""
        logger.debug("Checking if products page is loaded")

        # Check URL contains 'inventory'
        url_correct = "inventory.html" in self.driver.current_url

        # Check inventory container is visible
        element_visible = self.is_visible(self.INVENTORY_CONTAINER, timeout=5)

        is_loaded = url_correct and element_visible

        if is_loaded:
            logger.info("✅ Products page loaded successfully")
        else:
            logger.warning(
                f"⚠️ Products page not loaded - URL: {url_correct}, Element: {element_visible}"
            )

        return is_loaded

    def checkout_complete_is_loaded(self):
        """Check if checkout complete page is loaded"""
        logger.debug("Checking if checkout complete page is loaded")

        # Check URL contains 'inventory'
        url_correct = "checkout-complete" in self.driver.current_url

        # Check inventory container is visible
        element_visible = self.is_visible(self.COMPLETE_HEADER, timeout=5)

        is_loaded = url_correct and element_visible

        if is_loaded:
            logger.info("✅ Checkout complete page loaded successfully")
        else:
            logger.warning(
                f"⚠️ checkout complete not loaded - URL: {url_correct}, Element: {element_visible}"
            )

        return is_loaded

    def get_product_count(self):
        """Get number of products displayed"""
        logger.debug("Getting number of products displayed")

        try:
            # Find all product items
            elements = self.find_elements(self.INVENTORY_ITEMS)
            count = len(elements)

            logger.info(f"✅ Found {count} products on page")
            return count

        except Exception as e:
            logger.error(f"❌ Failed to get product count: {e}")
            return 0

    def get_product_names(self):
        """Get list of all product names"""
        logger.debug("Getting list of all product names")

        try:
            # Find all product name elements
            elements = self.find_elements(self.PRODUCT_NAMES)

            # Extract text from each element
            product_names = [element.text for element in elements]

            logger.info(f"✅ Found {len(product_names)} product names: {product_names}")
            return product_names  # ✅ Return list of names!

        except Exception as e:
            logger.error(f"❌ Failed to get product names: {e}")
            return []  # ❌ Return empty list on error

    def get_product_prices(self):
        """Get list of all product prices"""
        logger.debug("Getting list of all product prices")

        try:
            # Find all product name elements
            elements = self.find_elements(self.PRODUCT_PRICES)

            # Extract and convert in one line!
            product_prices = [
                float(element.text.replace("$", "")) for element in elements
            ]

            logger.info(
                f"✅ Found {len(product_prices)} product prices: {product_prices}"
            )
            return product_prices  # ✅ Return list of names!

        except Exception as e:
            logger.error(f"❌ Failed to get product prices: {e}")
            return []  # ❌ Return empty list on error

    def add_product_to_cart_by_name(self, product_name):
        """
        Add specific product to cart by name

        Args:
            product_name (str): Exact product name (e.g., "Sauce Labs Backpack")

        Returns:
            bool: True if successfully added, False otherwise
        """
        logger.debug(f"Adding product to cart: {product_name}")

        try:
            # Find all product items
            products = self.find_elements(self.INVENTORY_ITEMS)
            logger.debug(f"Found {len(products)} products on page")

            # Loop through products to find matching name
            for index, product in enumerate(products, 1):
                # Get product name
                name_element = product.find_element(
                    By.CLASS_NAME, "inventory_item_name"
                )
                current_name = name_element.text

                logger.debug(f"Product {index}: '{current_name}'")

                if current_name == product_name:
                    # Found the product! Click add to cart button
                    add_button = product.find_element(
                        By.CSS_SELECTOR, "button[id^='add-to-cart']"
                    )

                    # Use JavaScript click for reliability in headless mode
                    self.driver.execute_script("arguments[0].click();", add_button)
                    logger.debug("Clicked add to cart button using JavaScript")

                    # Wait for cart badge to appear
                    try:
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located(self.SHOPPING_CART_BADGE)
                        )
                        logger.debug("✅ Cart badge appeared")
                    except Exception as e:  # ✅ Fixed: was bare except
                        logger.warning(
                            f"⚠️ Cart badge did not appear after 5 seconds: {e}"
                        )

                    logger.info(f"✅ Successfully added '{product_name}' to cart")
                    return True

            # If we get here, product wasn't found
            logger.warning(f"⚠️ Product '{product_name}' not found on page")
            return False

        except Exception as e:
            logger.error(f"❌ Failed to add '{product_name}' to cart: {e}")
            import traceback

            logger.error(traceback.format_exc())
            return False

    def get_cart_badge_count(self):
        """Get number shown on shopping cart badge. Returns 0 if cart is empty."""
        try:
            # Try to find visible badge (wait up to 5 seconds)
            badge = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.SHOPPING_CART_BADGE)
            )

            # Get and clean the text
            count_text = badge.text.strip().strip("()")
            count = int(count_text)

            logger.info(f"✅ Cart has {count} items")
            return count

        except Exception as e:
            # Badge doesn't exist = cart is empty
            logger.debug(f"No badge found (cart empty): {e}")
            return 0

    def select_sort_option(self, option):
        """Select sort option from dropdown"""
        logger.debug(f"Selecting sort option: {option}")

        try:
            # Find and select
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.SORT_DROPDOWN)
            )

            select = Select(dropdown)
            select.select_by_value(option)

            # Wait for sort to apply
            time.sleep(2)

            # Verify (but this time, if it fails, we actually fail!)
            dropdown_new = self.find_element(self.SORT_DROPDOWN)
            select_new = Select(dropdown_new)
            actual_value = select_new.first_selected_option.get_attribute("value")

            if actual_value != option:
                raise Exception(f"Sort failed! Expected {option}, got {actual_value}")

            logger.info(f"✅ Successfully sorted by: {option}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to select sort option '{option}': {e}")
            return False

    def click_badge_count(self):
        """Click on shopping cart badge. Returns 0 if not successful"""
        try:
            try:
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.ESCAPE)
            except Exception as e:
                logger.debug(f"No popup to dismiss: {e}")
                pass
            # Try to find visible badge (wait up to 5 seconds)
            badge = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.SHOPPING_CART_BADGE)
            )
            badge.click()
            logger.info("✅ Badge click successfully")

        except Exception as e:
            # Badge doesn't exist
            logger.debug(f"❌ No badge found: {e}")
            return 0

    def click_button(self, button_id):
        f"""Click on {button_id}. Returns 0 if not successful"""
        try:
            badge = None
            # Try to find visible checkout button (wait up to 5 seconds)
            if button_id == "checkout":
                badge = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.CHECKOUT_BUTTON)
                )
            elif button_id == "continue":
                badge = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.CHECKOUT_CONTINUE_BUTTON)
                )
            elif button_id == "finish":
                badge = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.FINISH_BUTTON)
                )
            elif button_id == "back":
                badge = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.BACK_HOME_BUTTON)
                )

            badge.click()
            logger.info(f"✅ {button_id} click successfully")

        except Exception as e:
            # Continue button not found
            logger.debug(f"❌ No {button_id} button found: {e}")
            return 0

    def enter_first_name(self, first_name="first_name"):
        """Enter first name in first name field"""
        try:
            logger.info("Entering first name field")
            self.send_keys(self.FIRST_NAME_INPUT, first_name)
        except Exception as e:
            # First name field not found
            logger.debug(f"❌ No first name field found: {e}")
            return 0

    def enter_last_name(self, last_name="last_name"):
        """Enter last_name in last name field"""
        try:
            logger.info("Entering last name field")
            self.send_keys(self.LAST_NAME_INPUT, last_name)
        except Exception as e:
            # Last name field not found
            logger.debug(f"❌ No last name field found: {e}")
            return 0

    def enter_postal_code(self, postal_code="postal_code"):
        """Enter postal code in postal code field"""
        try:
            logger.info("Entering postal code field")
            self.send_keys(self.POSTAL_CODE, postal_code)
        except Exception as e:
            # Postal code field not found
            logger.debug(f"❌ No postal code field found: {e}")
            return 0
