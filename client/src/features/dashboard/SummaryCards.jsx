/**
 * SummaryCards component.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S2 (S2-05)
 * Requirement IDs: TMA-F-033
 */

import React from 'react'

export default function SummaryCards({ summary }) {
  const cards = [
    { title: 'Pending Tasks', count: summary?.pending ?? 0, color: '#f59e0b' },
    { title: 'In Progress', count: summary?.in_progress ?? 0, color: '#3b82f6' },
    { title: 'Completed', count: summary?.completed ?? 0, color: '#10b981' },
  ]

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
      {cards.map((c) => (
        <div key={c.title} className="card" style={{ borderTop: `4px solid ${c.color}` }}>
          <h4 className="text-muted" style={{ fontSize: '0.875rem', marginBottom: '0.5rem' }}>{c.title}</h4>
          <span style={{ fontSize: '2rem', fontWeight: 700 }}>{c.count}</span>
        </div>
      ))}
    </div>
  )
}

