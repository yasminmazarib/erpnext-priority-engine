def test_dashboard_page_loads(browser):
    """
    UI test: verify that the Dashboard page loads successfully.
    Uses shared Playwright browser fixture (headed locally, headless in CI).
    """

    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:3000/dashboard")

    assert page.url.endswith("/dashboard")

    context.close()
