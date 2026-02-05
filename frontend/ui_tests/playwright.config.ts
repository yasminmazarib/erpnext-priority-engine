import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',

    // חובה ב-CI (אין X server)
    headless: true,
  },

  // 🔑 זה התיקון הקריטי להתנגשות על פורט 3000
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: true, // ⬅️ אם כבר רץ – Playwright לא ירים שוב
    timeout: 120 * 1000,
  },
});
