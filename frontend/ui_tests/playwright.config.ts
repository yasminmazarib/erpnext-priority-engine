/// <reference types="node" />

import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    headless: true,
  },

  // ✅ webServer תקין + TypeScript מרוצה
  webServer: [
    {
      command: 'npm run dev',
      url: 'http://localhost:3000',
      reuseExistingServer: true,
      timeout: 60_000,
      cwd: '../', // ⬅️ חשוב: מפעיל את Next.js מתוך frontend
    },
  ],
});