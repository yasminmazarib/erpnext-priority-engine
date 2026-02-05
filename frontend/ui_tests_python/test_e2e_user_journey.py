import os
from playwright.sync_api import sync_playwright, expect
from ui_tests_python.dashboard_page import DashboardPage


def test_e2e_user_journey_apply_filter():
    base_url = os.getenv("BASE_URL", "http://localhost:3000")
    is_ci = os.getenv("CI", "false").lower() == "true"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=is_ci,
            slow_mo=0 if is_ci else 1000
        )

        page = browser.new_page()
        dashboard = DashboardPage(page)

        dashboard.open(base_url)
        dashboard.apply_filters()
        expect(dashboard.invoice_table()).to_be_visible()

        # רק בלוקאלי – משאירים את המסך פתוח 10 שניות
        if not is_ci:
            page.wait_for_timeout(10000)

        browser.close()


if __name__ == "__main__":
    test_e2e_user_journey_apply_filter()
