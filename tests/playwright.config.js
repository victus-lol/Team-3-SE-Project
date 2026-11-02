import { defineConfig, devices } from '@playwright/test'

/**
 * Playwright E2E configuration.
 * Owner: Akash Pawar (PES2UG24CS041)
 *
 * Run from tests/ with npm test. The working directory for both servers is
 * explicitly set to the repository root so paths work on Windows and CI.
 */
export default defineConfig({
  testDir: './e2e',
  timeout: 30000,
  expect: {
    timeout: 10000,
  },
  fullyParallel: false,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
  ],
  outputDir: 'test-results',
  use: {
    baseURL: 'http://127.0.0.1:5173',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: [
    {
      command: 'python tests/e2e/start_server.py',
      cwd: '..',
      url: 'http://127.0.0.1:5000/api/ready',
      timeout: 120000,
      reuseExistingServer: false,
      env: {
        FLASK_ENV: 'e2e',
        FLASK_HOST: '127.0.0.1',
      },
    },
    {
      command: 'npm --prefix client run dev -- --host 127.0.0.1',
      cwd: '..',
      url: 'http://127.0.0.1:5173/login',
      timeout: 120000,
      reuseExistingServer: !process.env.CI,
    },
  ],
})
