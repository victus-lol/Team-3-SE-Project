import React from 'react'
import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import TaskCard from '../features/tasks/TaskCard.jsx'

function localDateOffset(days) {
  const date = new Date()
  date.setDate(date.getDate() + days)
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${date.getFullYear()}-${month}-${day}`
}

describe('TaskCard', () => {
  it('labels an incomplete task with a past due date as overdue', () => {
    render(<MemoryRouter><TaskCard task={{ id: 8, title: 'Late task', status: 'pending', due_date: localDateOffset(-1) }} /></MemoryRouter>)

    expect(screen.getByText('Overdue')).toBeInTheDocument()
  })

  it('does not label a completed task as overdue', () => {
    render(<MemoryRouter><TaskCard task={{ id: 9, title: 'Completed task', status: 'completed', due_date: localDateOffset(-1) }} /></MemoryRouter>)

    expect(screen.queryByText('Overdue')).not.toBeInTheDocument()
  })
})
