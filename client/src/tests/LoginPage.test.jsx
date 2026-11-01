import React from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import LoginPage from '../features/auth/LoginPage.jsx'

const mocks = vi.hoisted(() => ({ login: vi.fn() }))

vi.mock('../features/auth/AuthContext.jsx', () => ({
  useAuth: () => ({ login: mocks.login }),
}))

function renderLogin() {
  return render(
    <MemoryRouter initialEntries={['/login']}>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<p>Dashboard destination</p>} />
      </Routes>
    </MemoryRouter>
  )
}

describe('LoginPage', () => {
  beforeEach(() => mocks.login.mockReset())

  it('submits credentials and returns to the protected destination', async () => {
    const user = userEvent.setup()
    mocks.login.mockResolvedValue({ success: true })
    renderLogin()

    await user.type(screen.getByLabelText(/email address/i), 'demo@example.com')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /continue to workspace/i }))

    expect(mocks.login).toHaveBeenCalledWith('demo@example.com', 'password123')
    expect(await screen.findByText('Dashboard destination')).toBeInTheDocument()
  })

  it('shows the backend error when credentials are rejected', async () => {
    const user = userEvent.setup()
    mocks.login.mockResolvedValue({ success: false, error: 'Invalid email or password.' })
    renderLogin()

    await user.type(screen.getByLabelText(/email address/i), 'wrong@example.com')
    await user.type(screen.getByLabelText(/password/i), 'wrong-password')
    await user.click(screen.getByRole('button', { name: /continue to workspace/i }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid email or password.')
  })
})
