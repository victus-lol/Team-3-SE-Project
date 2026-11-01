import React from 'react'
import Icon from '../../components/Icon.jsx'

const cards = [
  { key: 'pending', title: 'To do', note: 'Ready when you are', icon: 'clock', className: 'summary-pending' },
  { key: 'in_progress', title: 'In progress', note: 'Currently underway', icon: 'spark', className: 'summary-active' },
  { key: 'completed', title: 'Completed', note: 'Finished with care', icon: 'check', className: 'summary-complete' },
]

export default function SummaryCards({ summary }) {
  return (
    <div className="summary-grid">
      {cards.map((card) => (
        <article className={`card summary-card ${card.className}`} key={card.key}>
          <div className="summary-card-top">
            <span className="summary-label">{card.title}</span>
            <span className="summary-icon"><Icon name={card.icon} size={16} /></span>
          </div>
          <strong className="summary-value">{summary ? (summary[card.key] ?? 0) : '—'}</strong>
          <p className="summary-note">{summary ? card.note : 'Awaiting task data'}</p>
        </article>
      ))}
    </div>
  )
}
