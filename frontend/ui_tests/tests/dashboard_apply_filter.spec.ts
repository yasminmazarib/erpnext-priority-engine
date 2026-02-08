import { test } from '@playwright/test';
import { DashboardPage } from '../pages/DashboardPage';

test('Dashboard – Apply Filter displays invoice table', async ({ page }) => {

  // 🔹 Mock API response
  await page.route('**/priority/issues**', route => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        top_issues: [
          {
            invoice_id: 'INV-002',
            customer: 'Filter Test Customer',
            amount: 800,
            days_overdue: 3,
            priority: 'MEDIUM'
          }
        ]
      })
    });
  });

  const dashboard = new DashboardPage(page);

  // Step 1: Open dashboard
  await dashboard.open();

  // Step 2: Apply filter
  await dashboard.clickApplyFilters();

  // Step 3: Verify results
  await dashboard.expectInvoiceTableVisible();
});
