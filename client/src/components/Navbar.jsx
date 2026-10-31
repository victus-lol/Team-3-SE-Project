/**
 * Navbar component (skeleton).
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-06)
 *
 * TODO: Implement navigation links and logout button.
 */

import React from 'react'

export default function Navbar() {
  return (
    <nav
      style={{
        background: '#1d4ed8',
        color: '#fff',
        padding: '0.75rem 1rem',
        display: 'flex',
        alignItems: 'center',
        gap: '1rem',
      }}
    >
      <span style={{ fontWeight: 700, fontSize: '1.125rem' }}>Task Manager</span>
      {/* TODO (S1-06 — Aaryan): Add nav links and auth-aware logout */}
    </nav>
  )
}

