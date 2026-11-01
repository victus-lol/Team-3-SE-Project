import React from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import DashboardPage from '../features/dashboard/DashboardPage.jsx'

const mocks = vi.hoisted(() => ({ getSummary: vi.fn(), getTasks: vi.fn() }))

vi.mock('../features/auth/AuthContext.jsx', () => ({
  useAuth: () => ({ user: { name: 'Alex Rivera' } }),
}))
vi.mock('../services/api.js', () => ({ default: { get: mocks.getSummary } }))
vi.mock('../features/tasks/taskApi.js', () => ({ default: { getTasks: mocks.getTasks } }))

const tasks = [
  { id: 1, title: 'Finish report', status: 'pending', priority: 'high', due_date: '2030-05-15' },
  { id: 2, title: 'Review notes', status: 'in_progress', priority: 'medium', due_date: null },
  { id: 3, title: 'Archive project', status: 'completed', priority: 'low', due_date: null },
]

describe('DashboardPage', () => {
  beforeEach(() => {
    mocks.getSummary.mockReset().mockResolvedValue({ ok: true, data: { success: true, data: { pending: 1, in_progress: 1, completed: 1 } } })
    mocks.getTasks.mockReset().mockResolvedValue({ ok: true, data: { success: true, data: tasks } })
  })

  it('renders API summary metrics and open tasks', async () => {
    render(<MemoryRouter><DashboardPage /></MemoryRouter>)

    expect(await screen.findByText(/Alex/)).toBeInTheDocument()
    const pendingCard = screen.getByText('To do').closest('article')
    expect(within(pendingCard).getByText('1')).toBeInTheDocument()
    expect(screen.getByText('Finish report')).toBeInTheDocument()
    expect(screen.getByText('Review notes')).toBeInTheDocument()
    expect(screen.queryByText('Archive project')).not.toBeInTheDocument()
  })

  it('derives counts from task results when summary endpoint is unavailable', async () => {
    mocks.getSummary.mockResolvedValue({ ok: false, data: { error: { message: 'Summary unavailable' } } })
    render(<MemoryRouter><DashboardPage /></MemoryRouter>)

    expect(await screen.findByText(/Alex/)).toBeInTheDocument()
    const completedCard = screen.getByText('Completed').closest('article')
    expect(within(completedCard).getByText('1')).toBeInTheDocument()
  })
})
