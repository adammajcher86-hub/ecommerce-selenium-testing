"""
Configuration file for Selenium tests
"""

import os

# Base URL
BASE_URL = "https://www.saucedemo.com/"

# Test Users (from SauceDemo documentation)
STANDARD_USER = {"username": "standard_user", "password": "secret_sauce"}

LOCKED_OUT_USER = {"username": "locked_out_user", "password": "secret_sauce"}

PROBLEM_USER = {"username": "problem_user", "password": "secret_sauce"}

PERFORMANCE_GLITCH_USER = {
    "username": "performance_glitch_user",
    "password": "secret_sauce",
}

# Browser Configuration
DEFAULT_BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

# Timeouts (in seconds)
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15
PAGE_LOAD_TIMEOUT = 30

# Screenshots
SCREENSHOT_ON_FAILURE = True
SCREENSHOT_DIR = "screenshots"

# Window Size
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
