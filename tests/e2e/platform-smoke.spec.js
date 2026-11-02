import { test, expect } from '@playwright/test'

const API_BASE_URL = 'http://127.0.0.1:5000'

test.describe('Platform smoke and anonymous access checks', () => {
  test('API health endpoint reports that the service is alive', async ({ request }) => {
    const response = await request.get(`${API_BASE_URL}/api/health`)

    expect(response.status()).toBe(200)
    await expect(response).toBeOK()
    await expect(response).toBeTruthy()

    const body = await response.json()
    expect(body).toMatchObject({
      status: 'ok',
      service: 'task-manager-api',
    })
  })

  test('API readiness endpoint confirms database connectivity', async ({ request }) => {
    const response = await request.get(`${API_BASE_URL}/api/ready`)

    expect(response.status()).toBe(200)
    const body = await response.json()
    expect(body.success).toBe(true)
    expect(body.data).toMatchObject({ db: 'ok' })
  })

  test('public sign-in page renders its required fields', async ({ page }) => {
    await page.goto('/login')

    await expect(page.getByRole('heading', { name: 'Sign in' })).toBeVisible()
    await expect(page.getByLabel('Email address')).toBeVisible()
    await expect(page.getByLabel('Password')).toBeVisible()
    await expect(page.getByRole('button', { name: /continue to workspace/i })).toBeVisible()
  })

  test('private workspace routes redirect logged-out visitors to sign in', async ({ page }) => {
    for (const path of ['/dashboard', '/tasks', '/notifications', '/admin']) {
      await page.goto(path)
      await expect(page).toHaveURL(/\/login$/)
      await expect(page.getByRole('heading', { name: 'Sign in' })).toBeVisible()
    }
  })

  test('task, notification, and admin APIs reject anonymous requests', async ({ request }) => {
    const protectedPaths = [
      '/api/tasks',
      '/api/notifications',
      '/api/admin/users',
    ]

    for (const path of protectedPaths) {
      const response = await request.get(`${API_BASE_URL}${path}`)
      expect(response.status(), `${path} must reject anonymous access`).toBe(401)

      const body = await response.json()
      expect(body.success).toBe(false)
    }
  })
})
