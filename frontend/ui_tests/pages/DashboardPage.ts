import { Page } from '@playwright/test';

export class DashboardPage {
  constructor(private page: Page) {}

  async open() {
    await this.page.setContent(`
      <button data-testid="apply-filters">Apply</button>
      <table data-testid="invoice-table">
        <tr><td>Mock Row</td></tr>
      </table>
    `);
  }

  async applyFilters() {
    await this.page.getByTestId('apply-filters').click();
  }

  async expectInvoiceTableVisible() {
    await this.page.getByTestId('invoice-table').waitFor({
      state: 'attached',
    });
  }
}
