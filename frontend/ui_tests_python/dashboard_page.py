class DashboardPage:
    def __init__(self, page):
        self.page = page

    def open(self, base_url):
        self.page.goto(f"{base_url}/dashboard")

    def apply_filters(self):
        self.page.get_by_test_id("apply-filters").click()

    def invoice_table(self):
        return self.page.get_by_test_id("invoice-table")
