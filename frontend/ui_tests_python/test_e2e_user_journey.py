import os
from playwright.sync_api import expect
from ui_tests_python.dashboard_page import DashboardPage


def test_e2e_user_journey_apply_filter(browser):
    """
    E2E UI test:
    User opens dashboard and applies filters.
    Verifies UI reacts (table OR empty state).
    Stable for CI without real data dependency.
    """

    base_url = os.getenv("BASE_URL", "http://localhost:3000")

    context = browser.new_context()
    page = context.new_page()

    dashboard = DashboardPage(page)

    dashboard.open(base_url)
    dashboard.apply_filters()

    # UI must react: either table appears OR empty state message
    table = dashboard.invoice_table()
    empty_state = page.get_by_text("No invoices found")

    expect(
        table.or_(empty_state)
    ).to_be_visible(timeout=15000)

    context.close()
