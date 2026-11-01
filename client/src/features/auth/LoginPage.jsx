import React, { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from './AuthContext.jsx'
import Icon from '../../components/Icon.jsx'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [formError, setFormError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const from = location.state?.from?.pathname || '/dashboard'

  const handleSubmit = async (event) => {
    event.preventDefault()
    setFormError('')
    setSubmitting(true)
    try {
      const result = await login(email.trim(), password)
      if (result.success) navigate(from, { replace: true })
      else setFormError(result.error || 'We could not verify those details.')
    } catch (error) {
      setFormError(error.message || 'The sign-in service is unavailable. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="login-page">
      <section className="login-story" aria-label="Task Manager introduction">
        <div className="brand-lockup">
          <div className="brand-mark"><Icon name="check" size={22} strokeWidth={2.1} /></div>
          <div><p className="brand-wordmark">Task Manager</p><p className="brand-caption">Personal workspace</p></div>
        </div>
        <div className="login-story-copy">
          <p className="eyebrow">Plan with purpose</p>
          <h1>Make space for meaningful progress.</h1>
          <p>Bring your priorities into focus, keep important work moving, and build a clear rhythm for the things you want to accomplish.</p>
        </div>
        <div className="login-story-footer">A considered space for everyday work.</div>
      </section>

      <section className="login-panel">
        <div className="login-form-wrap">
          <p className="eyebrow">Welcome back</p>
          <h2>Sign in</h2>
          <p className="login-form-intro">Use your account credentials to continue to your workspace.</p>
          {formError && <div className="error-message" role="alert">{formError}</div>}
          <form className="form-grid" onSubmit={handleSubmit}>
            <div className="form-field">
              <label htmlFor="email">Email address</label>
              <input id="email" name="email" type="email" autoComplete="username" value={email} onChange={(event) => setEmail(event.target.value)} required />
            </div>
            <div className="form-field">
              <label htmlFor="password">Password</label>
              <input id="password" name="password" type="password" autoComplete="current-password" value={password} onChange={(event) => setPassword(event.target.value)} required />
            </div>
            <button className="btn btn-primary login-submit" type="submit" disabled={submitting}>
              {submitting ? 'Signing in…' : <>Continue to workspace <Icon name="arrow" size={15} /></>}
            </button>
          </form>
          <p className="login-footnote">Accounts are provisioned by your project administrator.</p>
        </div>
      </section>
    </main>
  )
}
