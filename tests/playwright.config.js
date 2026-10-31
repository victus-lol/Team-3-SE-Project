import { defineConfig, devices } from '@playwright/test'

/**
 * Playwright E2E configuration.
 * Owner: Akash Pawar (PES2UG24CS041)
 *
 * Configured with webServer to automatically launch:
 * 1. Flask backend on port 5000 (with temporary test DB)
 * 2. Vite frontend on port 5173
 * No manual orchestration or Docker required!
 */

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  fullyParallel: false,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: [
    {
      command: 'python server/run.py',
      port: 5000,
      timeout: 120000,
      reuseExistingServer: !process.env.CI,
      env: {
        FLASK_ENV: 'testing',
        DATABASE_URL: 'sqlite:///instance/e2e_test.sqlite',
      },
    },
    {
      command: 'npm --prefix client run dev',
      port: 5173,
      timeout: 120000,
      reuseExistingServer: !process.env.CI,
    },
  ],
})

