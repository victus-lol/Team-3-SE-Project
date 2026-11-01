import React from 'react'
import { Link } from 'react-router-dom'
import Icon from '../../components/Icon.jsx'

function formatDate(value) {
  if (!value) return 'No due date'
  const date = new Date(`${value}T00:00:00`)
  return Number.isNaN(date.valueOf()) ? value : new Intl.DateTimeFormat('en', { month: 'short', day: 'numeric', year: 'numeric' }).format(date)
}

export default function TaskCard({ task, onDelete, onEdit }) {
  const dueDate = task.due_date ? new Date(`${task.due_date}T00:00:00`) : null
  const isOverdue = dueDate && dueDate < new Date(new Date().setHours(0, 0, 0, 0)) && task.status !== 'completed'

  return (
    <article className="card task-card">
      <span className={`task-status-mark ${task.status || 'pending'}`} aria-hidden="true" />
      <div className="task-card-main">
        <Link to={`/tasks/${task.id}`} className="task-card-title">{task.title}</Link>
        {task.description && <p className="task-card-description">{task.description}</p>}
        <div className="task-card-meta">
          <span className={`pill priority-${task.priority || 'medium'}`}>{task.priority || 'medium'} priority</span>
          <span className={`pill status-${task.status || 'pending'}`}>{(task.status || 'pending').replace('_', ' ')}</span>
          <span className={`pill${isOverdue ? ' priority-high' : ''}`}><Icon name="calendar" size={12} /> {isOverdue ? 'Overdue' : formatDate(task.due_date)}</span>
        </div>
      </div>
      <div className="task-card-actions">
        <button className="icon-button" type="button" aria-label={`Edit ${task.title}`} title="Edit task" onClick={() => onEdit?.(task)}><Icon name="edit" size={15} /></button>
        <button className="icon-button danger" type="button" aria-label={`Delete ${task.title}`} title="Delete task" onClick={() => onDelete?.(task.id)}><Icon name="trash" size={15} /></button>
      </div>
    </article>
  )
}
