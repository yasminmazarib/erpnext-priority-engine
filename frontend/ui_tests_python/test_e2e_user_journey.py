import os
from playwright.sync_api import expect
from ui_tests_python.dashboard_page import DashboardPage


def test_e2e_user_journey_apply_filter(browser):
    """
    E2E UI test:
    User opens dashboard, applies filters, and sees invoice table.
    Robust for CI latency.
    """

    base_url = os.getenv("BASE_URL", "http://localhost:3000")

    context = browser.new_context()
    page = context.new_page()

    dashboard = DashboardPage(page)

    dashboard.open(base_url)
    dashboard.apply_filters()

    # ⬅️ חשוב: להמתין עד שהטבלה תופיע (CI איטי)
    invoice_table = dashboard.invoice_table()
    expect(invoice_table).to_be_attached(timeout=15000)
    expect(invoice_table).to_be_visible(timeout=15000)

    context.close()
