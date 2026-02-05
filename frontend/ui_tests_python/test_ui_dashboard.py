from playwright.sync_api import sync_playwright


def test_dashboard_page_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=1000   # ⬅️ האטה של שנייה בין פעולות
        )
        context = browser.new_context()
        page = context.new_page()

        page.goto("http://localhost:3000/dashboard")

        assert page.url.endswith("/dashboard")

        browser.close()
