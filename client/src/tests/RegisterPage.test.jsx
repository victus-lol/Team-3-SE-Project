import React from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import RegisterPage from '../features/auth/RegisterPage.jsx'

const mocks = vi.hoisted(() => ({ post: vi.fn() }))

vi.mock('../services/api.js', () => ({ default: { post: mocks.post } }))

function renderRegister() {
  return render(
    <MemoryRouter initialEntries={['/register']}>
      <Routes>
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<p>Sign-in destination</p>} />
      </Routes>
    </MemoryRouter>
  )
}

describe('RegisterPage', () => {
  beforeEach(() => mocks.post.mockReset())

  it('creates a standard account and returns to sign in', async () => {
    const user = userEvent.setup()
    mocks.post.mockResolvedValue({ ok: true, data: { success: true } })
    renderRegister()

    await user.type(screen.getByLabelText(/full name/i), 'New User')
    await user.type(screen.getByLabelText(/email address/i), 'new@example.com')
    await user.type(screen.getByLabelText(/password/i), 'securepass123')
    await user.click(screen.getByRole('button', { name: /create account/i }))

    expect(mocks.post).toHaveBeenCalledWith('/auth/register', {
      name: 'New User',
      email: 'new@example.com',
      password: 'securepass123',
    })
    expect(await screen.findByText('Sign-in destination')).toBeInTheDocument()
  })

  it('shows an API validation error', async () => {
    const user = userEvent.setup()
    mocks.post.mockResolvedValue({ ok: false, data: { error: { message: 'An account with this email already exists.' } } })
    renderRegister()

    await user.type(screen.getByLabelText(/full name/i), 'New User')
    await user.type(screen.getByLabelText(/email address/i), 'used@example.com')
    await user.type(screen.getByLabelText(/password/i), 'securepass123')
    await user.click(screen.getByRole('button', { name: /create account/i }))

    expect(await screen.findByRole('alert')).toHaveTextContent('An account with this email already exists.')
  })
})
