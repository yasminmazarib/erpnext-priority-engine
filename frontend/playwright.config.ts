import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './ui_tests/tests',
  timeout: 30_000,

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    headless: true,
  },

  webServer: {
    command: 'npm run build && npm run start',
    port: 3000,
    timeout: 120_000,
    reuseExistingServer: !process.env.CI,
  },
});
