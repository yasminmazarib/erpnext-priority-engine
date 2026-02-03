import os
from playwright.sync_api import sync_playwright, expect


def test_e2e_user_journey_apply_filter():
    # BASE_URL:
    # לוקאלית -> http://localhost:3000 או 3001
    # CI -> יגיע מ-ngrok
    base_url = os.getenv("BASE_URL", "http://localhost:3000")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Step 1: Open dashboard
        page.goto(f"{base_url}/dashboard")

        # Step 2: User applies filter
        page.get_by_test_id("apply-filters").click()

        # Step 3: Validate result
        expect(page.get_by_test_id("invoice-table")).to_be_visible()

        browser.close()
