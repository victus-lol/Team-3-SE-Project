/**
 * LoginPage tests.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-07)
 * Requirement IDs: TMA-F-001
 */

import React from 'react'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from '../features/auth/AuthContext.jsx'
import LoginPage from '../features/auth/LoginPage.jsx'

describe('LoginPage', () => {
  it.skip('renders email and password inputs and submits credentials', () => {
    // TC-Auth-01 | Owner: Aaryan | Requirement: TMA-F-001 | Backlog: S1-07
    render(
      <BrowserRouter>
        <AuthProvider>
          <LoginPage />
        </AuthProvider>
      </BrowserRouter>
    )
    expect(screen.getByLabelText(/Email Address/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument()
  })

  it.skip('shows validation error when fields are empty', () => {
    // TC-Auth-02 | Owner: Aaryan | Requirement: TMA-F-001 | Backlog: S1-07
  })
})

