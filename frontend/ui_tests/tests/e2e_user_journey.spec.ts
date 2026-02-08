import { test } from '@playwright/test';
import { DashboardPage } from '../pages/DashboardPage';

test('E2E User Journey – Apply Filters shows invoice table', async ({ page }) => {

  // 🔹 Mock API response
  await page.route('**/priority/issues**', route => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        top_issues: [
          {
            invoice_id: 'INV-001',
            customer: 'Mock Customer Ltd',
            amount: 1200,
            days_overdue: 7,
            priority: 'HIGH'
          }
        ]
      })
    });
  });

  // 🔹 Page Object
  const dashboard = new DashboardPage(page);

  // Step 1: Open dashboard
  await dashboard.open();

  // Step 2: Apply filter feature
  await dashboard.clickApplyFilters();

  // Step 3: Validate results
  await dashboard.expectInvoiceTableVisible();
});
