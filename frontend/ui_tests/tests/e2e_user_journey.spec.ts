import { test } from '@playwright/test';
import { DashboardPage } from '../pages/DashboardPage';

test('E2E user journey – dashboard shows invoice table', async ({ page }) => {
  const dashboard = new DashboardPage(page);

  // Step 1: Open dashboard
  await dashboard.open();

  // Step 2: Click Apply Filters (user action)
  await dashboard.clickApplyFilters();

  // Step 3: Verify invoice table is visible
  await dashboard.expectInvoiceTableVisible();
});
