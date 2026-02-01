import { Page, Locator } from '@playwright/test';

export class DashboardPage {
  readonly page: Page;
  readonly applyFiltersButton: Locator;
  readonly invoiceTable: Locator;

  constructor(page: Page) {
    this.page = page;
    this.applyFiltersButton = page.getByTestId('apply-filters');
    this.invoiceTable = page.getByTestId('invoice-table');
  }

  async open() {
    // ❌ לא localhost
    // ✅ דף יחסי
    await this.page.goto('/');
  }

  async applyFilters() {
    await this.applyFiltersButton.click();
  }

  async expectInvoiceTableVisible() {
    await this.invoiceTable.waitFor({ state: 'visible' });
  }
}
