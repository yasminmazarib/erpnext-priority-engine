import os
from playwright.sync_api import expect
from ui_tests_python.dashboard_page import DashboardPage


def test_e2e_user_journey_apply_filter(browser):
    """
    E2E UI test:
    User opens dashboard, applies filters, and sees invoice table.
    Uses shared Playwright browser fixture (headed locally, headless in CI).
    """

    base_url = os.getenv("BASE_URL", "http://localhost:3000")

    context = browser.new_context()
    page = context.new_page()

    dashboard = DashboardPage(page)

    dashboard.open(base_url)
    dashboard.apply_filters()
    expect(dashboard.invoice_table()).to_be_visible()

    context.close()
