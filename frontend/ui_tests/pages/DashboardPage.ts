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
    await this.page.goto('http://localhost:3000/dashboard');
  }

  async clickApplyFilters() {
    await this.applyFiltersButton.click();
  }

  async expectInvoiceTableVisible() {
    await this.invoiceTable.waitFor({ state: 'visible' });
  }
}
