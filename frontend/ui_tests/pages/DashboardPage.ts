export class DashboardPage {
  constructor(private page: Page) {}

  async open() {
    await this.page.goto('http://localhost:3000/dashboard');
  }

  async applyFilters() {
    await this.page.getByTestId('apply-filters').click();
  }

  async isInvoiceTableVisible() {
    await this.page.getByTestId('invoice-table').waitFor();
  }
}
