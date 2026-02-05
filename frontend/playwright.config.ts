import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './ui_tests/tests',
  timeout: 30_000,

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    headless: true,
  },
});