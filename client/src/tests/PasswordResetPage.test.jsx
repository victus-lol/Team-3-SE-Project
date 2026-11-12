import React from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import PasswordResetPage from '../features/auth/PasswordResetPage.jsx'
import authApi from '../features/auth/authApi.js'

vi.mock('../features/auth/authApi.js', () => ({
  default: {
    requestPasswordReset: vi.fn(),
    confirmPasswordReset: vi.fn(),
  },
}))

function renderPage(path = '/reset-password') {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="/reset-password" element={<PasswordResetPage />} />
        <Route path="/login" element={<p>Sign-in page</p>} />
      </Routes>
    </MemoryRouter>,
  )
}

describe('PasswordResetPage', () => {
  beforeEach(() => vi.clearAllMocks())

  it('requests a reset link with a privacy-preserving confirmation', async () => {
    authApi.requestPasswordReset.mockResolvedValue({ ok: true, data: { success: true } })
    renderPage()

    fireEvent.change(screen.getByLabelText('Email address'), { target: { value: 'person@example.com' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send reset link' }))

    await waitFor(() => expect(authApi.requestPasswordReset).toHaveBeenCalledWith('person@example.com'))
    expect(await screen.findByRole('status')).toHaveTextContent('If an account matches that address')
  })

  it('submits a token to set a new password and links back to sign in', async () => {
    authApi.confirmPasswordReset.mockResolvedValue({ ok: true, data: { success: true } })
    renderPage('/reset-password?token=single-use-token')

    fireEvent.change(screen.getByLabelText('New password'), { target: { value: 'newpassword123' } })
    fireEvent.click(screen.getByRole('button', { name: 'Update password' }))

    await waitFor(() => expect(authApi.confirmPasswordReset).toHaveBeenCalledWith('single-use-token', 'newpassword123'))
    expect(await screen.findByRole('status')).toHaveTextContent('Your password has been updated')
    fireEvent.click(screen.getByRole('link', { name: 'Return to sign in' }))
    expect(await screen.findByText('Sign-in page')).toBeInTheDocument()
  })
})
