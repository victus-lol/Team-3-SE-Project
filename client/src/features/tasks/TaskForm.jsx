/**
 * TaskForm component — Create / Edit task.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-08)
 * Requirement IDs: TMA-F-010, TMA-F-011, TMA-F-020
 */

import React, { useState } from 'react'
import taskApi from './taskApi.js'

export default function TaskForm({ isOpen, onClose, onSuccess, initialData }) {
  const [title, setTitle] = useState(initialData?.title || '')
  const [description, setDescription] = useState(initialData?.description || '')
  const [priority, setPriority] = useState(initialData?.priority || 'medium')
  const [status, setStatus] = useState(initialData?.status || 'pending')
  const [dueDate, setDueDate] = useState(initialData?.due_date || '')
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  if (!isOpen) return null

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setSubmitting(true)

    const payload = {
      title,
      description: description || null,
      priority,
      status,
      due_date: dueDate || null,
    }

    try {
      let res
      if (initialData?.id) {
        res = await taskApi.updateTask(initialData.id, payload)
      } else {
        res = await taskApi.createTask(payload)
      }

      if (res.ok && res.data?.success) {
        onSuccess()
      } else {
        setError(res.data?.error?.message || 'Failed to save task')
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex',
      alignItems: 'center', justifyContent: 'center', zIndex: 1000
    }}>
      <div className="card" style={{ maxWidth: '500px', width: '100%', margin: '1rem' }}>
        <h3 style={{ marginBottom: '1rem' }}>{initialData ? 'Edit Task' : 'New Task'}</h3>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <label htmlFor="task-title" style={{ display: 'block', marginBottom: '0.25rem', fontWeight: 500 }}>
              Title *
            </label>
            <input
              id="task-title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              style={{ width: '100%', padding: '0.5rem', border: '1px solid var(--color-border)', borderRadius: 'var(--radius)' }}
              required
              maxLength={200}
            />
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label htmlFor="task-desc" style={{ display: 'block', marginBottom: '0.25rem', fontWeight: 500 }}>
              Description
            </label>
            <textarea
              id="task-desc"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              style={{ width: '100%', padding: '0.5rem', border: '1px solid var(--color-border)', borderRadius: 'var(--radius)', minHeight: '80px' }}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
            <div>
              <label htmlFor="task-priority" style={{ display: 'block', marginBottom: '0.25rem', fontWeight: 500 }}>
                Priority
              </label>
              <select
                id="task-priority"
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                style={{ width: '100%', padding: '0.5rem', border: '1px solid var(--color-border)', borderRadius: 'var(--radius)' }}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            <div>
              <label htmlFor="task-status" style={{ display: 'block', marginBottom: '0.25rem', fontWeight: 500 }}>
                Status
              </label>
              <select
                id="task-status"
                value={status}
                onChange={(e) => setStatus(e.target.value)}
                style={{ width: '100%', padding: '0.5rem', border: '1px solid var(--color-border)', borderRadius: 'var(--radius)' }}
              >
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label htmlFor="task-due-date" style={{ display: 'block', marginBottom: '0.25rem', fontWeight: 500 }}>
              Due Date
            </label>
            <input
              id="task-due-date"
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              style={{ width: '100%', padding: '0.5rem', border: '1px solid var(--color-border)', borderRadius: 'var(--radius)' }}
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
            <button type="button" className="btn" onClick={onClose} disabled={submitting}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Saving...' : initialData ? 'Update Task' : 'Create Task'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

