import React from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import NotificationPanel from '../features/notifications/NotificationPanel.jsx'

const mocks = vi.hoisted(() => ({ get: vi.fn(), patch: vi.fn() }))

vi.mock('../services/api.js', () => ({
  default: { get: mocks.get, patch: mocks.patch },
}))

describe('NotificationPanel', () => {
  beforeEach(() => {
    mocks.get.mockReset().mockResolvedValue({ ok: true, data: { success: true, data: [
      { id: 4, message: 'A task is due tomorrow', status: 'pending' },
    ] } })
    mocks.patch.mockReset().mockResolvedValue({ ok: true, data: { success: true } })
  })

  it('loads notifications and marks one as read', async () => {
    const user = userEvent.setup()
    render(<NotificationPanel />)

    expect(await screen.findByText('A task is due tomorrow')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: /mark as read/i }))

    expect(mocks.patch).toHaveBeenCalledWith('/notifications/4/read', {})
    expect(await screen.findByText('Read')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /mark as read/i })).not.toBeInTheDocument()
  })

  it('shows a clear state when the notifications API is unavailable', async () => {
    mocks.get.mockResolvedValue({ ok: false, data: { error: { message: 'Notification listing is not implemented.' } } })
    render(<NotificationPanel />)

    expect(await screen.findByText(/Notification listing is not implemented/)).toBeInTheDocument()
  })
})
