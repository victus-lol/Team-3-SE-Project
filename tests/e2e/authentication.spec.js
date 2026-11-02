import { test, expect } from '@playwright/test'

/**
 * Authentication E2E tests.
 * Owner: Akash Pawar (PES2UG24CS041)
 * Sprint: S2 (S2-09)
 * Requirement IDs: TMA-F-001, TMA-F-002
 */

test.describe('Authentication Flow', () => {
  test('valid user login and logout', async ({ page }) => {
    // TC-Auth-01 | Owner: Akash | Requirement: TMA-F-001 | Backlog: S2-09
    await page.goto('/login')
    await page.getByLabel('Email address').fill('e2e.user@example.com')
    await page.getByLabel('Password').fill('password123')
    await page.getByRole('button', { name: /continue to workspace/i }).click()

    await expect(page).toHaveURL(/\/dashboard$/)
    await expect(page.getByText('E2E Test User', { exact: true })).toBeVisible()

    await page.getByRole('button', { name: /sign out/i }).click()
    await expect(page).toHaveURL(/\/login$/)
    await expect(page.getByRole('heading', { name: 'Sign in' })).toBeVisible()
  })

  test('invalid credentials are rejected with an error message', async ({ page }) => {
    // TC-Auth-02 | Owner: Akash | Requirement: TMA-F-001 | Backlog: S2-09
    await page.goto('/login')
    await page.getByLabel('Email address').fill('unknown.e2e.user@example.com')
    await page.getByLabel('Password').fill('incorrect-password')
    await page.getByRole('button', { name: /continue to workspace/i }).click()

    await expect(page.getByRole('alert')).toContainText('Invalid email or password.')
    await expect(page).toHaveURL(/\/login$/)
  })

  test('protected page redirects to login when logged out', async ({ page }) => {
    // TC-Auth-03 | Owner: Akash | Requirement: TMA-F-002 | Backlog: S2-09
    await page.goto('/dashboard')

    await expect(page).toHaveURL(/\/login$/)
    await expect(page.getByRole('heading', { name: 'Sign in' })).toBeVisible()
  })
})
