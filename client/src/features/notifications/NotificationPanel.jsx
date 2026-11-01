import React, { useCallback, useEffect, useState } from 'react'
import api from '../../services/api.js'
import Loading from '../../components/Loading.jsx'
import Icon from '../../components/Icon.jsx'

export default function NotificationPanel() {
  const [notifications, setNotifications] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [busyId, setBusyId] = useState(null)

  const loadNotifications = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const res = await api.get('/notifications')
      if (res.ok && res.data?.success && Array.isArray(res.data.data)) {
        setNotifications(res.data.data)
      } else {
        setNotifications([])
        setError(res.data?.error?.message || 'Notifications are not available yet.')
      }
    } catch (err) {
      setNotifications([])
      setError(err.message || 'Could not reach the notification service.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { loadNotifications() }, [loadNotifications])

  const markAsRead = async (id) => {
    setBusyId(id)
    setError('')
    try {
      const res = await api.patch(`/notifications/${id}/read`, {})
      if (res.ok && res.data?.success) {
        setNotifications((current) => current.map((item) => item.id === id ? { ...item, status: 'read' } : item))
      } else {
        setError(res.data?.error?.message || 'This notification could not be updated.')
      }
    } catch (err) {
      setError(err.message || 'Could not reach the notification service.')
    } finally {
      setBusyId(null)
    }
  }

  if (loading) return <Loading message="Loading notifications..." />

  return (
    <>
      <div className="page-heading">
        <div>
          <p className="eyebrow">Workspace / Updates</p>
          <h1 className="page-title">Notifications</h1>
          <p className="page-subtitle">Reminders and updates related to your tasks.</p>
        </div>
        <button className="btn btn-quiet" type="button" onClick={loadNotifications}><Icon name="clock" size={15} /> Refresh</button>
      </div>

      {error ? (
        <div className="notice" role="status">
          {error} The notification API in this local project is still awaiting implementation.
        </div>
      ) : notifications.length === 0 ? (
        <div className="card empty-state"><Icon name="bell" size={23} /><strong>You’re all caught up</strong><p>New reminders and updates will appear here.</p></div>
      ) : (
        <section className="card panel" aria-label="Notifications">
          <div className="task-preview-list">
            {notifications.map((notification) => (
              <article className="task-preview" key={notification.id}>
                <span className={`task-dot ${notification.status === 'read' ? '' : 'in_progress'}`} />
                <span className="task-preview-copy"><strong>{notification.message}</strong><span>{notification.status === 'read' ? 'Read' : 'Unread'}</span></span>
                {notification.status !== 'read' && (
                  <button className="btn btn-quiet" type="button" onClick={() => markAsRead(notification.id)} disabled={busyId === notification.id}>
                    {busyId === notification.id ? 'Updating…' : 'Mark as read'}
                  </button>
                )}
              </article>
            ))}
          </div>
          {error && <div className="error-message" role="alert" style={{ marginTop: 14 }}>{error}</div>}
        </section>
      )}
    </>
  )
}
