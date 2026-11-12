import { test, expect } from '@playwright/test'
import { signIn } from './helpers.js'

/**
 * Reminders and Notifications E2E tests.
 * Owner: Akash Pawar (PES2UG24CS041)
 * Sprint: S2 (S2-09)
 * Requirement IDs: TMA-F-040, TMA-F-041
 */

test.describe('Reminders and Notifications Flow', () => {
  test('view notification alerts in panel', async ({ page }) => {
    await signIn(page)
    await page.goto('/notifications')
    await expect(page.getByText('E2E reminder for notification workflow')).toBeVisible()
  })

  test('mark a notification as read updates status', async ({ page }) => {
    await signIn(page)
    await page.goto('/notifications')
    const reminder = page.locator('.task-preview').filter({ hasText: 'E2E unread reminder for read-state workflow' })
    await reminder.getByRole('button', { name: 'Mark as read' }).click()
    await expect(reminder.getByText('Read', { exact: true })).toBeVisible()
    await expect(reminder.getByRole('button', { name: 'Mark as read' })).toHaveCount(0)
  })
})

