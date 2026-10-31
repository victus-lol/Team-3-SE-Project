/**
 * HealthStatus — home shell component, shows API connection status.
 * Calls GET /api/health and displays the result.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-06) — Part of foundation, always live.
 */

import React, { useEffect, useState } from 'react'
import api from '../services/api.js'

export default function HealthStatus() {
  const [status, setStatus] = useState('checking')
  const [error, setError] = useState(null)

  useEffect(() => {
    api
      .get('/health')
      .then(({ data, ok }) => {
        if (ok && data?.status === 'ok') {
          setStatus('connected')
        } else {
          setStatus('error')
          setError('Unexpected response from API.')
        }
      })
      .catch((err) => {
        setStatus('error')
        setError(err.message || 'Could not reach the API.')
      })
  }, [])

  return (
    <div className="container" style={{ padding: '2rem' }}>
      <h1 style={{ marginBottom: '1rem' }}>Task Manager</h1>
      <div className="card">
        <h2 style={{ marginBottom: '0.5rem' }}>API Status</h2>
        {status === 'checking' && <p className="text-muted">Connecting to API…</p>}
        {status === 'connected' && (
          <p className="success-message">✓ Connected to task-manager-api</p>
        )}
        {status === 'error' && (
          <p className="error-message">✗ {error || 'Failed to connect to API.'}</p>
        )}
        <p style={{ marginTop: '1rem', color: '#6b7280', fontSize: '0.875rem' }}>
          Feature modules are under development. Visit{' '}
          <a href="/login">Login</a> when authentication is implemented.
        </p>
      </div>
    </div>
  )
}

