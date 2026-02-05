import os
from playwright.sync_api import sync_playwright
import pytest

@pytest.fixture(scope="session")
def browser():
    headless = os.getenv("CI", "false").lower() == "true"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        yield browser
        browser.close()
