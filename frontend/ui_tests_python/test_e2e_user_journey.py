import os
from playwright.sync_api import sync_playwright, expect
from pages.dashboard_page import DashboardPage


def test_e2e_user_journey_apply_filter():
    base_url = os.getenv("BASE_URL", "http://localhost:3000")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        dashboard = DashboardPage(page)

        dashboard.open(base_url)
        dashboard.apply_filters()
        expect(dashboard.invoice_table()).to_be_visible()

        browser.close()