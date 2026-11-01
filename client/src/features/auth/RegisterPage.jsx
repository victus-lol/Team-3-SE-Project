/**
 * RegisterPage component (Scope-pending).
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 / Scope-pending
 *
 * NOTE: Registration acceptance criteria are pending approval.
 * See docs/DECISIONS_AND_OPEN_QUESTIONS.md item (1).
 */

import React from 'react'
import { Link } from 'react-router-dom'

export default function RegisterPage() {
  return (
    <div className="container" style={{ maxWidth: '400px', marginTop: '4rem' }}>
      <div className="card">
        <h2 style={{ marginBottom: '1rem', textAlign: 'center' }}>Create Account</h2>
        <div className="error-message" style={{ backgroundColor: '#fffbeb', borderColor: '#fef3c7', color: '#b45309' }}>
          Registration functionality is currently scope-pending. Contact an administrator to create your account.
        </div>
        <p style={{ marginTop: '1rem', textAlign: 'center', fontSize: '0.875rem' }} className="text-muted">
          Already have an account? <Link to="/login">Sign In</Link>
        </p>
      </div>
    </div>
  )
}

