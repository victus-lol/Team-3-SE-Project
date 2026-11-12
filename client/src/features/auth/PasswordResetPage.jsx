import React, { useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import authApi from './authApi.js'
import Icon from '../../components/Icon.jsx'

export default function PasswordResetPage() {
  const [params] = useSearchParams()
  const token = params.get('token') || ''
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setMessage('')
    setError('')
    setSubmitting(true)
    try {
      const response = token
        ? await authApi.confirmPasswordReset(token, password)
        : await authApi.requestPasswordReset(email.trim())
      if (!response.ok || !response.data?.success) {
        setError(response.data?.error?.message || 'We could not complete that request. Please try again.')
      } else if (token) {
        setMessage('Your password has been updated. Sign in with your new password.')
      } else {
        setMessage('If an account matches that address, a reset link will be sent.')
      }
    } catch (requestError) {
      setError(requestError.message || 'The account recovery service is unavailable. Please try again.')
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
        <div className="login-story-copy"><p className="eyebrow">Account recovery</p><h1>Return to a clear plan.</h1><p>Use a secure, time-limited link to restore access to your workspace.</p></div>
        <div className="login-story-footer">A considered space for everyday work.</div>
      </section>
      <section className="login-panel">
        <div className="login-form-wrap">
          <p className="eyebrow">{token ? 'Choose a new password' : 'Secure access'}</p>
          <h2>{token ? 'Reset password' : 'Forgot password'}</h2>
          <p className="login-form-intro">{token ? 'Set a new password to secure your account.' : 'Enter the email address associated with your account.'}</p>
          {message && <div className="notice" role="status">{message}</div>}
          {error && <div className="error-message" role="alert">{error}</div>}
          {!message.includes('password has been updated') && (
            <form className="form-grid" onSubmit={handleSubmit}>
              {token ? (
                <div className="form-field"><label htmlFor="new-password">New password</label><input id="new-password" name="password" type="password" autoComplete="new-password" minLength={8} maxLength={128} value={password} onChange={(event) => setPassword(event.target.value)} required /><small>Use at least 8 characters.</small></div>
              ) : (
                <div className="form-field"><label htmlFor="recovery-email">Email address</label><input id="recovery-email" name="email" type="email" autoComplete="email" maxLength={254} value={email} onChange={(event) => setEmail(event.target.value)} required /></div>
              )}
              <button className="btn btn-primary login-submit" type="submit" disabled={submitting}>{submitting ? 'Please wait…' : token ? 'Update password' : 'Send reset link'}</button>
            </form>
          )}
          <p className="login-footnote"><Link to="/login">Return to sign in</Link></p>
        </div>
      </section>
    </main>
  )
}
