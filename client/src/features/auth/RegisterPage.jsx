import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../../services/api.js'
import Icon from '../../components/Icon.jsx'

export default function RegisterPage() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      const response = await api.post('/auth/register', { name: name.trim(), email: email.trim(), password })
      if (response.ok && response.data?.success) {
        navigate('/login', { replace: true, state: { notice: 'Your account is ready. Sign in to continue.' } })
      } else {
        setError(response.data?.error?.message || 'We could not create your account.')
      }
    } catch (requestError) {
      setError(requestError.message || 'The account service is unavailable. Please try again.')
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
        <div className="login-story-copy"><p className="eyebrow">A clear place to begin</p><h1>Build a rhythm for your work.</h1><p>Create a personal account to organize priorities, track progress, and keep your next step in view.</p></div>
        <div className="login-story-footer">A considered space for everyday work.</div>
      </section>
      <section className="login-panel">
        <div className="login-form-wrap">
          <p className="eyebrow">Get started</p>
          <h2>Create account</h2>
          <p className="login-form-intro">Use your email address to create a standard user account.</p>
          {error && <div className="error-message" role="alert">{error}</div>}
          <form className="form-grid" onSubmit={handleSubmit}>
            <div className="form-field"><label htmlFor="name">Full name</label><input id="name" name="name" autoComplete="name" maxLength={128} value={name} onChange={(event) => setName(event.target.value)} required /></div>
            <div className="form-field"><label htmlFor="email">Email address</label><input id="email" name="email" type="email" autoComplete="email" maxLength={254} value={email} onChange={(event) => setEmail(event.target.value)} required /></div>
            <div className="form-field"><label htmlFor="password">Password</label><input id="password" name="password" type="password" autoComplete="new-password" minLength={8} maxLength={128} value={password} onChange={(event) => setPassword(event.target.value)} required /><small>Use at least 8 characters.</small></div>
            <button className="btn btn-primary login-submit" type="submit" disabled={submitting}>{submitting ? 'Creating account…' : <>Create account <Icon name="arrow" size={15} /></>}</button>
          </form>
          <p className="login-footnote">Already have an account? <Link to="/login">Sign in</Link></p>
        </div>
      </section>
    </main>
  )
}

