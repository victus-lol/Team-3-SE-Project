/**
 * Loading component — shown during lazy-loaded route suspense.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 */

import React from 'react'

export default function Loading({ message = 'Loading...' }) {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '200px',
        flexDirection: 'column',
        gap: '1rem',
      }}
      role="status"
      aria-live="polite"
    >
      <div
        style={{
          width: '2rem',
          height: '2rem',
          border: '3px solid #e5e7eb',
          borderTop: '3px solid #2563eb',
          borderRadius: '50%',
          animation: 'spin 0.8s linear infinite',
        }}
      />
      <span style={{ color: '#6b7280', fontSize: '0.875rem' }}>{message}</span>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  )
}

