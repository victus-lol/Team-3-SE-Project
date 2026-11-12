import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

async function signIn(page) {
  await page.goto('/login')
  await page.getByLabel('Email address').fill('e2e.user@example.com')
  await page.getByLabel('Password').fill('password123')
  await page.getByRole('button', { name: /continue to workspace/i }).click()
  await expect(page).toHaveURL(/\/dashboard$/)
}

test.describe('Frontend feature workflows', () => {
  test('task CRUD and server-side search and filters work together', async ({ page }) => {
    await signIn(page)
    await page.goto('/tasks')

    await page.locator('.page-heading').getByRole('button', { name: 'Create task' }).click()
    const dialog = page.getByRole('dialog')
    await dialog.getByLabel('Task title').fill('E2E task lifecycle')
    await dialog.getByLabel('Description').fill('Verify search, filters, editing, and deletion')
    await dialog.getByLabel('Priority').selectOption('high')
    await dialog.getByLabel('Due date').fill('2020-01-01')
    await dialog.getByRole('button', { name: 'Create task' }).click()
    await expect(page.getByRole('link', { name: 'E2E task lifecycle' })).toBeVisible()

    const searchRequest = page.waitForRequest((request) => {
      const url = new URL(request.url())
      return url.pathname === '/api/tasks' && url.searchParams.get('q') === 'lifecycle'
    })
    const search = page.getByRole('searchbox', { name: 'Search tasks' })
    await search.fill('lifecycle')
    await search.press('Enter')
    await searchRequest
    await expect(page.getByRole('link', { name: 'E2E task lifecycle' })).toBeVisible()

    const filterRequest = page.waitForRequest((request) => {
      const url = new URL(request.url())
      return url.pathname === '/api/tasks' && url.searchParams.get('priority') === 'high'
    })
    await page.getByLabel('Filter by priority').selectOption('high')
    await filterRequest
    await expect(page.getByRole('link', { name: 'E2E task lifecycle' })).toBeVisible()

    const statusRequest = page.waitForRequest((request) => {
      const url = new URL(request.url())
      return url.pathname === '/api/tasks' && url.searchParams.get('status') === 'pending'
    })
    await page.getByLabel('Filter by status').selectOption('pending')
    await statusRequest

    const overdueRequest = page.waitForRequest((request) => {
      const url = new URL(request.url())
      return url.pathname === '/api/tasks' && url.searchParams.get('overdue') === 'true'
    })
    await page.getByLabel('Overdue').check()
    await overdueRequest
    await expect(page.getByRole('link', { name: 'E2E task lifecycle' })).toBeVisible()

    await page.getByRole('button', { name: 'Clear filters' }).click()
    await page.getByRole('link', { name: 'E2E task lifecycle' }).click()
    await expect(page.getByRole('heading', { name: 'E2E task lifecycle' })).toBeVisible()
    await page.getByRole('link', { name: /back to tasks/i }).click()

    await page.getByRole('button', { name: 'Edit E2E task lifecycle' }).click()
    const editDialog = page.getByRole('dialog')
    const titleField = editDialog.getByLabel('Task title')
    await titleField.fill('E2E task lifecycle updated')
    await editDialog.getByRole('button', { name: 'Save changes' }).click()
    await expect(page.getByRole('link', { name: 'E2E task lifecycle updated' })).toBeVisible()

    await page.getByRole('button', { name: 'Delete E2E task lifecycle updated' }).click()
    const confirm = page.getByRole('alertdialog')
    await expect(confirm).toBeVisible()
    await page.keyboard.press('Escape')
    await expect(confirm).not.toBeVisible()

    await page.getByRole('button', { name: 'Delete E2E task lifecycle updated' }).click()
    await page.getByRole('alertdialog').getByRole('button', { name: 'Delete task' }).click()
    await expect(page.getByRole('link', { name: 'E2E task lifecycle updated' })).toHaveCount(0)
  })

  test('dashboard summary renders from the live API', async ({ page }) => {
    await signIn(page)
    await expect(page.getByRole('heading', { name: 'At a glance' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'In focus' })).toBeVisible()
    await expect(page.getByText('Task data is currently unavailable from the API.')).toHaveCount(0)
  })

  test('notifications load and can be marked read through the live API', async ({ page }) => {
    await signIn(page)
    await page.getByRole('link', { name: 'Notifications' }).click()
    const reminder = page.locator('.task-preview').filter({ hasText: 'E2E reminder for notification workflow' })
    await expect(reminder).toBeVisible()
    await reminder.getByRole('button', { name: 'Mark as read' }).click()
    await expect(reminder.getByText('Read', { exact: true })).toBeVisible()
    await expect(reminder.getByRole('button', { name: 'Mark as read' })).toHaveCount(0)
  })

  test('workspace supports keyboard entry and narrow mobile widths', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 })
    await signIn(page)

    await page.evaluate(() => document.activeElement?.blur())
    await page.keyboard.press('Tab')
    await expect(page.getByRole('link', { name: 'Skip to main content' })).toBeFocused()
    await page.keyboard.press('Enter')
    await expect(page.locator('#main-content')).toBeFocused()

    for (const path of ['/dashboard', '/tasks', '/notifications']) {
      await page.goto(path)
      await expect.poll(() => page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)
    }

    await page.goto('/tasks')
    await page.locator('.page-heading').getByRole('button', { name: 'Create task' }).click()
    const dialog = page.getByRole('dialog')
    await expect(dialog.getByLabel('Task title')).toBeFocused()
    await page.keyboard.press('Shift+Tab')
    await expect(dialog.getByRole('button', { name: 'Close dialog' })).toBeFocused()
    await page.keyboard.press('Shift+Tab')
    await expect(dialog.getByRole('button', { name: 'Cancel' })).toBeFocused()
    await page.keyboard.press('Escape')
    await expect(dialog).not.toBeVisible()
    await expect(page.locator('.page-heading').getByRole('button', { name: 'Create task' })).toBeFocused()
  })

  test('core screens pass accessibility checks at mobile, tablet, and desktop widths', async ({ page }) => {
    test.setTimeout(90000)
    await page.emulateMedia({ reducedMotion: 'reduce' })
    const viewports = [
      { width: 375, height: 812 },
      { width: 768, height: 1024 },
      { width: 1440, height: 900 },
    ]

    for (const viewport of viewports) {
      await page.setViewportSize(viewport)
      await page.goto('/login')
      await expect(page.getByRole('heading', { name: 'Sign in' })).toBeVisible()
      let results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()
      expect(results.violations.map(({ id, help, nodes }) => ({ id, help, elements: nodes.map(({ html, failureSummary }) => ({ html, failureSummary })) }))).toEqual([])

      await signIn(page)
      for (const [path, heading] of [
        ['/dashboard', 'At a glance'],
        ['/tasks', 'My tasks'],
        ['/notifications', 'Notifications'],
      ]) {
        await page.goto(path)
        await expect(page.getByRole('heading', { name: heading })).toBeVisible()
        await expect.poll(() => page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)
        results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()
        expect(results.violations.map(({ id, help, nodes }) => ({ id, help, elements: nodes.map(({ html, failureSummary }) => ({ html, failureSummary })) }))).toEqual([])
      }
    }
  })
})
