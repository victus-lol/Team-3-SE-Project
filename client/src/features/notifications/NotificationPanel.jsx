/**
 * NotificationPanel component.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S2 (S2-08)
 * Requirement IDs: TMA-F-040, TMA-F-041
 */

import React, { useState, useEffect } from 'react'
import api from '../../services/api.js'
import Loading from '../../components/Loading.jsx'

export default function NotificationPanel() {
  const [notifications, setNotifications] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const res = await api.get('/notifications')
        if (res.ok && res.data?.success) {
          setNotifications(res.data.data)
        }
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const markAsRead = async (id) => {
    const res = await api.patch(`/notifications/${id}/read`, {})
    if (res.ok) {
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, status: 'read' } : n))
      )
    }
  }

  if (loading) return <Loading message="Loading notifications..." />

  return (
    <div className="card">
      <h3 style={{ marginBottom: '1rem' }}>Notifications</h3>
      {notifications.length === 0 ? (
        <p className="text-muted">No notifications right now.</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {notifications.map((n) => (
            <li
              key={n.id}
              style={{
                padding: '0.75rem 0',
                borderBottom: '1px solid var(--color-border)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                opacity: n.status === 'read' ? 0.6 : 1,
              }}
            >
              <span>{n.message}</span>
              {n.status !== 'read' && (
                <button
                  className="btn"
                  style={{ fontSize: '0.75rem' }}
                  onClick={() => markAsRead(n.id)}
                >
                  Mark as read
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

