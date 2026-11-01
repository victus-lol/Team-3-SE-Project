/**
 * Frontend Foundation tests.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-06)
 */

import React from 'react'
import { render, screen } from '@testing-library/react'
import { afterEach, beforeEach, vi } from 'vitest'
import Loading from '../components/Loading.jsx'
import App from '../app/App.jsx'

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn(async (url) => {
    const csrfRequest = String(url).endsWith('/api/auth/csrf')
    return {
      ok: csrfRequest,
      status: csrfRequest ? 200 : 501,
      headers: { get: () => 'application/json' },
      json: async () => csrfRequest
        ? { success: true, data: { csrf_token: 'test-csrf-token' } }
        : { success: false, error: { message: 'Current user is not implemented.' } },
    }
  }))
})

afterEach(() => vi.unstubAllGlobals())

describe('Frontend Foundation', () => {
  it('renders Loading spinner component with default message', () => {
    render(<Loading />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('renders Loading spinner with custom message', () => {
    render(<Loading message="Custom waiting..." />)
    expect(screen.getByText('Custom waiting...')).toBeInTheDocument()
  })

  it('redirects unauthenticated users to sign in', async () => {
    render(<App />)
    expect(await screen.findByRole('heading', { name: 'Sign in' })).toBeInTheDocument()
  })
})

