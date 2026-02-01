import { test } from '@playwright/test';
import { DashboardPage } from '../pages/DashboardPage';

test('E2E – user applies filters and sees results', async ({ page }) => {
  const dashboard = new DashboardPage(page);

  await dashboard.open();
  await dashboard.applyFilters();          // ← FEATURE
  await dashboard.isInvoiceTableVisible(); // ← תוצאה
});
