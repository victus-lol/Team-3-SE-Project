import React, { useState } from 'react'
import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import TaskFilters from '../features/search/TaskFilters.jsx'

function FilterHarness() {
  const [filters, setFilters] = useState({ status: '', priority: '', overdue: false })
  return <><TaskFilters filters={filters} onChange={setFilters} /><output>{JSON.stringify(filters)}</output></>
}

describe('TaskFilters', () => {
  it('updates the selected status filter', async () => {
    const user = userEvent.setup()
    render(<FilterHarness />)

    await user.selectOptions(screen.getByLabelText(/filter by status/i), 'in_progress')

    expect(screen.getByText('{"status":"in_progress","priority":"","overdue":false}')).toBeInTheDocument()
  })

  it('updates priority and overdue filters', async () => {
    const user = userEvent.setup()
    render(<FilterHarness />)

    await user.selectOptions(screen.getByLabelText(/filter by priority/i), 'high')
    await user.click(screen.getByLabelText(/overdue/i))

    expect(screen.getByText('{"status":"","priority":"high","overdue":true}')).toBeInTheDocument()
  })
})
