"""
Products Page Object Model
Represents the SauceDemo products/inventory page
"""

import logging
from selenium.webdriver.common.by import By
from pages.page_base import BasePage

logger = logging.getLogger(__name__)


class ProductsPage(BasePage):
    """Page Object for SauceDemo products page"""

    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

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
            return []  # ✅ Return empty list on error

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
            return []  # ✅ Return empty list on error

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

                    # Scroll to button (if needed)
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView(true);", add_button
                    )

                    add_button.click()

                    logger.info(f"✅ Successfully added '{product_name}' to cart")
                    return True

            # If we get here, product wasn't found
            logger.warning(f"⚠️ Product '{product_name}' not found on page")
            available_products = [
                p.find_element(By.CLASS_NAME, "inventory_item_name").text
                for p in products
            ]
            logger.debug(f"Available products: {available_products}")
            return False

        except Exception as e:
            logger.error(f"❌ Failed to add '{product_name}' to cart: {e}")
            return False

    def get_cart_badge_count(self):
        """
        Get number shown on shopping cart badge
        Returns 0 if cart is empty (no badge visible)
        """
        logger.debug("Getting cart badge count")

        try:
            # Badge only exists when cart has items
            if self.is_visible(self.SHOPPING_CART_BADGE, timeout=2):
                badge = self.find_element(self.SHOPPING_CART_BADGE)
                count = int(badge.text)
                logger.info(f"✅ Cart badge shows: {count} items")
                return count
            else:
                logger.info("✅ Cart is empty (no badge visible)")
                return 0

        except ValueError as e:
            logger.error(f"❌ Badge text is not a number: {e}")
            return 0
        except Exception as e:
            logger.error(f"❌ Failed to get cart badge count: {e}")
            return 0

    def select_sort_option(self, option):
        """
        Select sort option from dropdown

        Args:
            option (str): Sort option value
                - "az" = Name (A to Z)
                - "za" = Name (Z to A)
                - "lohi" = Price (low to high)
                - "hilo" = Price (high to low)

        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug(f"Selecting sort option: {option}")

        try:
            from selenium.webdriver.support.select import Select

            # Find dropdown
            dropdown_element = self.find_element(self.SORT_DROPDOWN)

            # Create Select object
            select = Select(dropdown_element)

            # Select by value
            select.select_by_value(option)

            # Get selected option for confirmation
            selected_option = select.first_selected_option
            logger.info(f"✅ Selected sort: '{selected_option.text}' (value: {option})")

            return True

        except Exception as e:
            logger.error(f"❌ Failed to select sort option '{option}': {e}")
            return False
