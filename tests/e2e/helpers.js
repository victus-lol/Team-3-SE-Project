import { expect } from '@playwright/test'

export async function signIn(page, email = 'e2e.user@example.com', password = 'password123') {
  await page.goto('/login')
  await page.getByLabel('Email address').fill(email)
  await page.getByLabel('Password').fill(password)
  await page.getByRole('button', { name: /continue to workspace/i }).click()
  await expect(page).toHaveURL(/\/dashboard$/)
}

export async function createTask(page, { title, priority = 'medium', status = 'pending' }) {
  await page.goto('/tasks')
  await page.locator('.page-heading').getByRole('button', { name: 'Create task' }).click()
  const dialog = page.getByRole('dialog')
  await dialog.getByLabel('Task title').fill(title)
  await dialog.getByLabel('Priority').selectOption(priority)
  await dialog.getByLabel('Status').selectOption(status)
  await dialog.getByRole('button', { name: 'Create task' }).click()
  await expect(page.getByRole('link', { name: title })).toBeVisible()
}
