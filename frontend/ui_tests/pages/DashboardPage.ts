import { Page, expect } from '@playwright/test';

export class DashboardPage {
  constructor(private page: Page) {}

  async open() {
    await this.page.goto('/dashboard');
  }

  async clickApplyFilters() {
    await this.page.getByTestId('apply-filters').click();
  }

  async expectInvoiceTableVisible() {
    await expect(
      this.page.getByTestId('invoice-table')
    ).toBeVisible();
  }
}
