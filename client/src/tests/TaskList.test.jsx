import React from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import TaskList from '../features/tasks/TaskList.jsx'

const mocks = vi.hoisted(() => ({ getTasks: vi.fn(), deleteTask: vi.fn() }))

vi.mock('../features/tasks/taskApi.js', () => ({
  default: { getTasks: mocks.getTasks, deleteTask: mocks.deleteTask },
}))

const sampleTasks = [
  { id: 1, title: 'Prepare slides', description: 'Project demo', status: 'in_progress', priority: 'high', due_date: '2030-05-15' },
  { id: 2, title: 'Read chapter', description: 'Unit 4', status: 'pending', priority: 'low', due_date: null },
]

function renderTaskList() {
  return render(<MemoryRouter><TaskList /></MemoryRouter>)
}

describe('TaskList', () => {
  beforeEach(() => {
    mocks.getTasks.mockReset().mockImplementation((criteria = {}) => {
      const normalizedQuery = criteria.q?.toLowerCase() || ''
      const data = sampleTasks.filter((task) => (
        (!normalizedQuery || `${task.title} ${task.description}`.toLowerCase().includes(normalizedQuery))
        && (!criteria.status || task.status === criteria.status)
        && (!criteria.priority || task.priority === criteria.priority)
      ))
      return Promise.resolve({ ok: true, data: { success: true, data } })
    })
    mocks.deleteTask.mockReset()
  })

  it('loads tasks and filters by a search query', async () => {
    const user = userEvent.setup()
    renderTaskList()

    expect(await screen.findByText('Prepare slides')).toBeInTheDocument()
    expect(screen.getByText('Read chapter')).toBeInTheDocument()
    const search = screen.getByRole('searchbox', { name: /search tasks/i })
    await user.type(search, 'slides')
    await user.keyboard('{Enter}')

    await waitFor(() => expect(mocks.getTasks).toHaveBeenLastCalledWith(expect.objectContaining({ q: 'slides' })))
    expect(screen.getByText('Prepare slides')).toBeInTheDocument()
    expect(screen.queryByText('Read chapter')).not.toBeInTheDocument()
  })

  it('sends selected filters to the API and can clear them', async () => {
    const user = userEvent.setup()
    renderTaskList()

    expect(await screen.findByText('Prepare slides')).toBeInTheDocument()
    await user.selectOptions(screen.getByLabelText('Filter by priority'), 'high')
    await waitFor(() => expect(mocks.getTasks).toHaveBeenLastCalledWith(expect.objectContaining({ priority: 'high' })))
    expect(screen.getByText('Prepare slides')).toBeInTheDocument()
    expect(screen.queryByText('Read chapter')).not.toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Clear filters' }))
    await waitFor(() => expect(mocks.getTasks).toHaveBeenLastCalledWith(expect.objectContaining({ priority: '' })))
    expect(await screen.findByText('Read chapter')).toBeInTheDocument()
  })

  it('asks for confirmation and deletes the selected task', async () => {
    const user = userEvent.setup()
    mocks.deleteTask.mockResolvedValue({ ok: true, data: { success: true } })
    renderTaskList()

    expect(await screen.findByText('Prepare slides')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Delete Prepare slides' }))
    expect(screen.getByRole('alertdialog')).toHaveTextContent('Prepare slides')
    await user.click(screen.getByRole('button', { name: /delete task/i }))

    await waitFor(() => expect(mocks.deleteTask).toHaveBeenCalledWith(1))
    await waitFor(() => expect(screen.queryByText('Prepare slides')).not.toBeInTheDocument())
  })

  it('offers a retry when task loading fails', async () => {
    const user = userEvent.setup()
    mocks.getTasks.mockResolvedValueOnce({ ok: false, data: { error: { message: 'Task service unavailable.' } } })
    renderTaskList()

    expect(await screen.findByText('Tasks could not be loaded')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Try again' }))
    expect(await screen.findByText('Prepare slides')).toBeInTheDocument()
  })
})
