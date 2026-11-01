/**
 * TaskFilters component.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S2 (S2-03)
 * Requirement IDs: TMA-F-021, TMA-F-022
 */

import React from 'react'

export default function TaskFilters({ filters, onChange }) {
  const handleChange = (key, value) => {
    onChange({ ...filters, [key]: value })
  }

  return (
    <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', margin: '1rem 0' }}>
      <select
        value={filters.status || ''}
        onChange={(e) => handleChange('status', e.target.value)}
        style={{ padding: '0.4rem', border: '1px solid var(--color-border)', borderRadius: 'var(--radius)' }}
      >
        <option value="">All Statuses</option>
        <option value="pending">Pending</option>
        <option value="in_progress">In Progress</option>
        <option value="completed">Completed</option>
      </select>

      <select
        value={filters.priority || ''}
        onChange={(e) => handleChange('priority', e.target.value)}
        style={{ padding: '0.4rem', border: '1px solid var(--color-border)', borderRadius: 'var(--radius)' }}
      >
        <option value="">All Priorities</option>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>

      <label style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', fontSize: '0.875rem' }}>
        <input
          type="checkbox"
          checked={Boolean(filters.overdue)}
          onChange={(e) => handleChange('overdue', e.target.checked ? 'true' : '')}
        />
        Overdue Only
      </label>
    </div>
  )
}

