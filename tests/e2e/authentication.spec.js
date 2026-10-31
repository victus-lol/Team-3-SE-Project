import { test, expect } from '@playwright/test'

/**
 * Authentication E2E tests.
 * Owner: Akash Pawar (PES2UG24CS041)
 * Sprint: S2 (S2-09)
 * Requirement IDs: TMA-F-001, TMA-F-002
 */

test.describe('Authentication Flow', () => {
  test.skip('valid user login and logout', async ({ page }) => {
    // TC-Auth-01 | Owner: Akash | Requirement: TMA-F-001 | Backlog: S2-09
    await page.goto('/login')
    await page.fill('#email', 'testuser@example.com')
    await page.fill('#password', 'password123')
    await page.click('button[type="submit"]')
    await expect(page).toHaveURL('/tasks')
  })

  test.skip('invalid credentials rejected with error message', async ({ page }) => {
    // TC-Auth-02 | Owner: Akash | Requirement: TMA-F-001 | Backlog: S2-09
  })

  test.skip('protected page redirects to login when logged out', async ({ page }) => {
    // TC-Auth-03 | Owner: Akash | Requirement: TMA-F-002 | Backlog: S2-09
  })
})

