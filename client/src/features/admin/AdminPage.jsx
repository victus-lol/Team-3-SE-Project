/**
 * AdminPage component.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S2 (S2-06)
 * Requirement IDs: TMA-SR-001
 */

import React, { useState, useEffect } from 'react'
import api from '../../services/api.js'
import Loading from '../../components/Loading.jsx'

export default function AdminPage() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function loadUsers() {
      try {
        const res = await api.get('/admin/users')
        if (res.ok && res.data?.success) {
          setUsers(res.data.data)
        } else {
          setError(res.data?.error?.message || 'Access denied or failed to load users.')
        }
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    loadUsers()
  }, [])

  return (
    <div className="container" style={{ padding: '2rem 1rem' }}>
      <h2 style={{ marginBottom: '1.5rem' }}>Administration: User Management</h2>
      {error && <div className="error-message">{error}</div>}
      {loading ? (
        <Loading message="Loading system users..." />
      ) : (
        <div className="card">
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid var(--color-border)' }}>
                <th style={{ padding: '0.5rem' }}>ID</th>
                <th style={{ padding: '0.5rem' }}>Name</th>
                <th style={{ padding: '0.5rem' }}>Email</th>
                <th style={{ padding: '0.5rem' }}>Role</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id} style={{ borderBottom: '1px solid var(--color-border)' }}>
                  <td style={{ padding: '0.5rem' }}>{u.id}</td>
                  <td style={{ padding: '0.5rem' }}>{u.name}</td>
                  <td style={{ padding: '0.5rem' }}>{u.email}</td>
                  <td style={{ padding: '0.5rem' }}>{u.role}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

