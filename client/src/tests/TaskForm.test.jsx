import React from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import TaskForm from '../features/tasks/TaskForm.jsx'

const mocks = vi.hoisted(() => ({ createTask: vi.fn(), updateTask: vi.fn() }))

vi.mock('../features/tasks/taskApi.js', () => ({
  default: { createTask: mocks.createTask, updateTask: mocks.updateTask },
}))

describe('TaskForm', () => {
  beforeEach(() => {
    mocks.createTask.mockReset()
    mocks.updateTask.mockReset()
  })

  it('creates a task with the entered values', async () => {
    const user = userEvent.setup()
    const onSuccess = vi.fn()
    mocks.createTask.mockResolvedValue({ ok: true, data: { success: true } })
    render(<TaskForm isOpen onClose={vi.fn()} onSuccess={onSuccess} />)

    await user.type(screen.getByLabelText(/task title/i), 'Review project')
    await user.type(screen.getByLabelText(/description/i), 'Check the frontend')
    await user.selectOptions(screen.getByLabelText(/priority/i), 'high')
    await user.click(screen.getByRole('button', { name: /create task/i }))

    expect(mocks.createTask).toHaveBeenCalledWith({
      title: 'Review project',
      description: 'Check the frontend',
      priority: 'high',
      status: 'pending',
      due_date: null,
    })
    expect(onSuccess).toHaveBeenCalledOnce()
  })

  it('updates an existing task', async () => {
    const user = userEvent.setup()
    const onSuccess = vi.fn()
    mocks.updateTask.mockResolvedValue({ ok: true, data: { success: true } })
    render(<TaskForm isOpen initialData={{ id: 7, title: 'Old title', priority: 'low', status: 'pending' }} onClose={vi.fn()} onSuccess={onSuccess} />)

    const title = screen.getByLabelText(/task title/i)
    await user.clear(title)
    await user.type(title, 'Updated title')
    await user.click(screen.getByRole('button', { name: /save changes/i }))

    expect(mocks.updateTask).toHaveBeenCalledWith(7, expect.objectContaining({ title: 'Updated title', priority: 'low' }))
    expect(onSuccess).toHaveBeenCalledOnce()
  })
})
