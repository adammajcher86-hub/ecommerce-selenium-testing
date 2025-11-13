"""
Products Tests for SauceDemo
"""

import pytest
import logging


from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from config.config import STANDARD_USER

logger = logging.getLogger(__name__)


class TestProducts:
    """Test suite for products functionality"""

    @pytest.mark.smoke
    @pytest.mark.products
    def test_products_page_loads_after_login(self, driver):
        """Test that products page loads after successful login"""
        logger.info("Testing products page loads after login")

        # Login
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(STANDARD_USER["username"], STANDARD_USER["password"])

        # Verify page loaded
        products_page = ProductsPage(driver)
        assert products_page.is_loaded(), "Products page should be loaded"

        logger.info("✅ Products page loaded successfully")

    @pytest.mark.products
    def test_all_products_displayed(self, driver):
        """Test that all 6 products are displayed"""
        logger.info("Testing all 6 products are displayed")

        # Login
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(STANDARD_USER["username"], STANDARD_USER["password"])

        # Check count
        products_page = ProductsPage(driver)
        count = products_page.get_product_count()

        assert count == 6, f"Expected 6 products, but got {count}"

        logger.info(f"✅ All {count} products displayed")

    @pytest.mark.products
    @pytest.mark.products
    def test_add_product_to_cart(self, driver):
        """Test adding a product to cart"""
        logger.info("Testing add product to cart")

        # Login
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(STANDARD_USER["username"], STANDARD_USER["password"])

        products_page = ProductsPage(driver)

        # Verify cart is empty
        initial_count = products_page.get_cart_badge_count()
        assert initial_count == 0, "Cart should be empty initially"

        # Add product
        success = products_page.add_product_to_cart_by_name("Sauce Labs Backpack")
        assert success, "Failed to add product to cart"

        # Verify cart updated
        new_count = products_page.get_cart_badge_count()
        assert new_count == 1, f"Cart should have 1 item, got {new_count}"

        logger.info("✅ Product added to cart successfully")

    @pytest.mark.products
    def test_add_multiple_products_to_cart(self, driver):
        """Test adding multiple products to cart"""
        logger.info("Testing add multiple products to cart")

        # Login
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(STANDARD_USER["username"], STANDARD_USER["password"])

        products_page = ProductsPage(driver)

        # Add 3 products
        products_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt",
        ]

        for product in products_to_add:
            success = products_page.add_product_to_cart_by_name(product)
            assert success, f"Failed to add {product}"

        # Verify cart has 3 items
        cart_count = products_page.get_cart_badge_count()
        assert cart_count == 3, f"Cart should have 3 items, got {cart_count}"

        logger.info("✅ Multiple products added successfully")

    @pytest.mark.products
    def test_sort_products_by_price_low_to_high(self, driver):
        """Test sorting products by price (low to high)"""
        logger.info("Testing sort by price low to high")

        # Login
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(STANDARD_USER["username"], STANDARD_USER["password"])

        products_page = ProductsPage(driver)

        # Sort by price low to high
        success = products_page.select_sort_option("lohi")
        assert success, "Failed to select sort option"

        # Get prices after sort
        prices = products_page.get_product_prices()

        # Verify sorted in ascending order
        assert prices == sorted(prices), f"Prices should be sorted ascending: {prices}"

        logger.info(f"✅ Products sorted correctly: {prices}")

    @pytest.mark.products
    def test_sort_products_by_name_z_to_a(self, driver):
        """Test sorting products by name (Z to A)"""
        logger.info("Testing sort by name Z to A")

        # Login
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(STANDARD_USER["username"], STANDARD_USER["password"])

        products_page = ProductsPage(driver)

        # Sort by name Z to A
        success = products_page.select_sort_option("za")
        assert success, "Failed to select sort option"

        # Get names after sort
        names = products_page.get_product_names()

        # Verify sorted in reverse alphabetical order
        assert names == sorted(
            names, reverse=True
        ), f"Names should be sorted Z to A: {names}"

        logger.info("✅ Products sorted correctly by name")
