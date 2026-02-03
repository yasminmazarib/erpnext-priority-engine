from playwright.sync_api import sync_playwright

def test_dashboard_page_loads():
    print("START PYTHON UI TEST")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("http://localhost:3000/dashboard")

        assert page.locator('[data-testid="invoice-table"]').is_visible()

        browser.close()

    print("PYTHON UI TEST PASSED")
