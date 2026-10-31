/**
 * LoginPage component.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-07)
 * Requirement IDs: TMA-F-001
 *
 * TODO checklist (S1-07):
 *   [ ] Form with email and password inputs
 *   [ ] Client-side validation (non-empty, valid format)
 *   [ ] Delegate login to AuthContext
 *   [ ] Error banner on rejection
 *   [ ] Redirect to original protected route on success
 */

import React, { useState } from 'react'
import { useNavigate, useLocation, Link } from 'react-router-dom'
import { useAuth } from './AuthContext.jsx'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [formError, setFormError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const from = location.state?.from?.pathname || '/tasks'

  const handleSubmit = async (e) => {
    e.preventDefault()
    setFormError('')
    if (!email || !password) {
      setFormError('Please enter both email and password.')
      return
    }

    const res = await login(email, password)
    if (res.success) {
      navigate(from, { replace: true })
    } else {
      setFormError(res.error || 'Invalid credentials')
    }
  }

  return (
    <div className="container" style={{ maxWidth: '400px', marginTop: '4rem' }}>
      <div className="card">
        <h2 style={{ marginBottom: '1.5rem', textAlign: 'center' }}>Sign In</h2>
        {formError && <div className="error-message" role="alert">{formError}</div>}
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <label htmlFor="email" style={{ display: 'block', marginBottom: '0.25rem', fontWeight: 500 }}>
              Email Address
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{ width: '100%', padding: '0.5rem', border: '1px solid var(--color-border)', borderRadius: 'var(--radius)' }}
              required
            />
          </div>
          <div style={{ marginBottom: '1.5rem' }}>
            <label htmlFor="password" style={{ display: 'block', marginBottom: '0.25rem', fontWeight: 500 }}>
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ width: '100%', padding: '0.5rem', border: '1px solid var(--color-border)', borderRadius: 'var(--radius)' }}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary" style={{ width: '100%', justifyContent: 'center' }}>
            Sign In
          </button>
        </form>
        <p style={{ marginTop: '1rem', textAlign: 'center', fontSize: '0.875rem' }} className="text-muted">
          Don&apos;t have an account? <Link to="/register">Register (Scope-pending)</Link>
        </p>
      </div>
    </div>
  )
}

