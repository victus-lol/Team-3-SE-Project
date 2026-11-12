import { test, expect } from '@playwright/test'
import { signIn } from './helpers.js'

/**
 * Admin Access E2E tests.
 * Owner: Akash Pawar (PES2UG24CS041)
 * Sprint: S2 (S2-09)
 * Requirement IDs: TMA-SR-001
 */

test.describe('Admin Access Flow', () => {
  test('standard user is rejected from admin route', async ({ page }) => {
    await signIn(page)
    await page.goto('/admin')
    await expect(page).toHaveURL(/\/dashboard$/)
    await expect(page.getByRole('heading', { name: /user management/i })).toHaveCount(0)
  })

  test('admin user can view registered users', async ({ page }) => {
    await signIn(page, 'e2e.admin@example.com', 'adminpassword123')
    await page.goto('/admin')
    await expect(page.getByRole('heading', { name: /user management/i })).toBeVisible()
    await expect(page.getByText('e2e.user@example.com')).toBeVisible()
    await expect(page.getByText('e2e.admin@example.com')).toBeVisible()
  })
})

