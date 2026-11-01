/**
 * TaskCard component.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-08)
 * Requirement IDs: TMA-F-010, TMA-F-011, TMA-F-020
 */

import React from 'react'

export default function TaskCard({ task, onDelete, onUpdate }) {
  const priorityColors = {
    low: '#10b981',
    medium: '#f59e0b',
    high: '#ef4444',
  }

  return (
    <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
          <h3 style={{ fontSize: '1.125rem' }}>{task.title}</h3>
          <span style={{
            fontSize: '0.75rem',
            padding: '0.15rem 0.5rem',
            borderRadius: '1rem',
            color: '#fff',
            backgroundColor: priorityColors[task.priority] || '#6b7280'
          }}>
            {task.priority}
          </span>
          <span style={{
            fontSize: '0.75rem',
            padding: '0.15rem 0.5rem',
            borderRadius: '1rem',
            border: '1px solid var(--color-border)',
            color: 'var(--color-text-muted)'
          }}>
            {task.status}
          </span>
        </div>
        {task.description && <p className="text-muted" style={{ fontSize: '0.875rem', marginBottom: '0.5rem' }}>{task.description}</p>}
        {task.due_date && <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>Due: {task.due_date}</p>}
      </div>

      <div style={{ display: 'flex', gap: '0.5rem' }}>
        <button className="btn" style={{ fontSize: '0.75rem' }} onClick={() => onUpdate && onUpdate(task)}>
          Edit
        </button>
        <button className="btn btn-danger" style={{ fontSize: '0.75rem' }} onClick={() => onDelete && onDelete(task.id)}>
          Delete
        </button>
      </div>
    </div>
  )
}

