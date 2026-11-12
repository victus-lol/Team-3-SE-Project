import React from 'react'
import Icon from '../../components/Icon.jsx'

export default function TaskFilters({ filters, onChange }) {
  const set = (key, value) => onChange((current) => ({ ...current, [key]: value }))
  const hasFilters = Boolean(filters.status || filters.priority || filters.overdue)

  return (
    <div className="filter-controls" role="group" aria-label="Filter tasks">
      <Icon name="sliders" size={15} />
      <select aria-label="Filter by status" value={filters.status} onChange={(event) => set('status', event.target.value)}>
        <option value="">All statuses</option>
        <option value="pending">To do</option>
        <option value="in_progress">In progress</option>
        <option value="completed">Completed</option>
      </select>
      <select aria-label="Filter by priority" value={filters.priority} onChange={(event) => set('priority', event.target.value)}>
        <option value="">All priorities</option>
        <option value="high">High priority</option>
        <option value="medium">Medium priority</option>
        <option value="low">Low priority</option>
      </select>
      <label className="filter-chip"><input type="checkbox" checked={filters.overdue} onChange={(event) => set('overdue', event.target.checked)} /> Overdue</label>
      <button className="text-link filter-reset" type="button" disabled={!hasFilters} onClick={() => onChange({ status: '', priority: '', overdue: false })}>Clear filters</button>
    </div>
  )
}
