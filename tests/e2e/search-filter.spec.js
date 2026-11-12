import { test, expect } from '@playwright/test'
import { createTask, signIn } from './helpers.js'

/**
 * Search and Filter E2E tests.
 * Owner: Akash Pawar (PES2UG24CS041)
 * Sprint: S2 (S2-09)
 * Requirement IDs: TMA-F-021, TMA-F-022, TMA-F-023
 */

test.describe('Search and Filter Flow', () => {
  test('search tasks by keyword in searchbar', async ({ page }) => {
    await signIn(page)
    const title = `E2E searchable ${Date.now()}`
    await createTask(page, { title })
    await page.getByRole('searchbox', { name: 'Search tasks' }).fill('searchable')
    await page.getByRole('searchbox', { name: 'Search tasks' }).press('Enter')
    await expect(page.getByRole('link', { name: title })).toBeVisible()
  })

  test('filter tasks by status and priority', async ({ page }) => {
    await signIn(page)
    const match = `E2E filter match ${Date.now()}`
    const other = `E2E filter other ${Date.now()}`
    await createTask(page, { title: match, priority: 'high', status: 'pending' })
    await createTask(page, { title: other, priority: 'low', status: 'completed' })
    await page.getByLabel('Filter by status').selectOption('pending')
    await page.getByLabel('Filter by priority').selectOption('high')
    await expect(page.getByRole('link', { name: match })).toBeVisible()
    await expect(page.getByRole('link', { name: other })).toHaveCount(0)
  })

  test('sort tasks deterministically through the API', async ({ page }) => {
    await signIn(page)
    const suffix = Date.now()
    for (const title of [`E2E sort B ${suffix}`, `E2E sort A ${suffix}`]) {
      const status = await page.evaluate(async (taskTitle) => {
        const response = await fetch('/api/tasks', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: taskTitle }),
        })
        return response.status
      }, title)
      expect(status).toBe(201)
    }
    const response = await page.evaluate(async () => {
      const result = await fetch('/api/tasks?sort_by=title&order=asc')
      return result.json()
    })
    const titles = response.data.map((task) => task.title).filter((title) => title.startsWith(`E2E sort `))
    expect(titles).toEqual([`E2E sort A ${suffix}`, `E2E sort B ${suffix}`])
  })
})

