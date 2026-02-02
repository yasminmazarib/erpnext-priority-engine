import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  use: {
    // ✅ CI / Local friendly
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    headless: true,
  },
});
