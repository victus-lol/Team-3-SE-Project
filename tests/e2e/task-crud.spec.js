import { test, expect } from '@playwright/test'
import { createTask, signIn } from './helpers.js'

/**
 * Task CRUD E2E tests.
 * Owner: Akash Pawar (PES2UG24CS041)
 * Sprint: S2 (S2-09)
 * Requirement IDs: TMA-F-010, TMA-F-011, TMA-F-012
 */

test.describe('Task CRUD Flow', () => {
  test('create a new task and see it listed', async ({ page }) => {
    await signIn(page)
    const title = `E2E create ${Date.now()}`
    await createTask(page, { title })
  })

  test('update an existing task status and priority', async ({ page }) => {
    await signIn(page)
    const title = `E2E update ${Date.now()}`
    await createTask(page, { title })
    await page.getByRole('button', { name: `Edit ${title}` }).click()
    const dialog = page.getByRole('dialog')
    await dialog.getByLabel('Priority').selectOption('high')
    await dialog.getByLabel('Status').selectOption('in_progress')
    await dialog.getByRole('button', { name: 'Save changes' }).click()
    const task = page.locator('.task-card').filter({ has: page.getByRole('link', { name: title }) })
    await expect(task.getByText('high priority')).toBeVisible()
    await expect(task.getByText('in progress')).toBeVisible()
  })

  test('delete a task after confirmation', async ({ page }) => {
    await signIn(page)
    const title = `E2E delete ${Date.now()}`
    await createTask(page, { title })
    await page.getByRole('button', { name: `Delete ${title}` }).click()
    const dialog = page.getByRole('alertdialog')
    await expect(dialog).toBeVisible()
    await dialog.getByRole('button', { name: 'Delete task' }).click()
    await expect(page.getByRole('link', { name: title })).toHaveCount(0)
  })
})

