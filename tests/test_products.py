"""
Products Tests for SauceDemo
"""

import pytest
import logging

logger = logging.getLogger(__name__)


class TestProducts:
    """Test suite for products functionality"""

    # TODO: Test 1
    @pytest.mark.smoke
    @pytest.mark.products
    def test_products_page_loads_after_login(self, driver):
        """Test that products page loads after successful login"""
        # Steps:
        # 1. Login
        # 2. Verify products page is loaded
        # 3. Verify products are displayed
        pass

    # TODO: Test 2
    @pytest.mark.products
    def test_all_products_displayed(self, driver):
        """Test that all 6 products are displayed"""
        # Steps:
        # 1. Login
        # 2. Count products
        # 3. Assert count == 6
        pass

    # TODO: Test 3
    @pytest.mark.products
    def test_add_product_to_cart(self, driver):
        """Test adding a product to cart"""
        # Steps:
        # 1. Login
        # 2. Add product to cart
        # 3. Verify cart badge shows "1"
        pass

    # TODO: Test 4
    @pytest.mark.products
    def test_add_multiple_products_to_cart(self, driver):
        """Test adding multiple products to cart"""
        # Steps:
        # 1. Login
        # 2. Add 3 different products
        # 3. Verify cart badge shows "3"
        pass

    # TODO: Test 5
    @pytest.mark.products
    def test_sort_products_by_price_low_to_high(self, driver):
        """Test sorting products by price (low to high)"""
        # Steps:
        # 1. Login
        # 2. Get initial prices
        # 3. Sort by "Price (low to high)"
        # 4. Get new prices
        # 5. Assert prices are in ascending order
        pass

    # TODO: Test 6 (Bonus)
    @pytest.mark.products
    def test_sort_products_by_name_z_to_a(self, driver):
        """Test sorting products by name (Z to A)"""
        # Similar to test 5, but for names
        pass
