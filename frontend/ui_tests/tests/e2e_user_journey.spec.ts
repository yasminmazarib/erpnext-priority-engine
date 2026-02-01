import { test } from '@playwright/test';
import { DashboardPage } from '../pages/DashboardPage';

test('E2E User Journey – Apply Filters shows invoice table', async ({ page }) => {

  // 🔹 MOCK ל-API
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

  const dashboard = new DashboardPage(page);

  // Step 1: Open page
  await dashboard.open();

  // Step 2: Apply filters (FEATURE)
  await dashboard.applyFilters();

  // Step 3: Assert result
  await dashboard.expectInvoiceTableVisible();
});
