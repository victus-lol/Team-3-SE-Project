import { beforeEach, describe, expect, it, vi } from 'vitest'

describe('CSRF token initialization', () => {
  beforeEach(() => {
    vi.resetModules()
  })

  it('shares one in-flight token request between concurrent app initializations', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ success: true, data: { csrf_token: 'session-token' } }),
    })
    vi.stubGlobal('fetch', fetchMock)
    const csrf = await import('../services/csrf.js')

    const tokens = await Promise.all([
      csrf.fetchCsrfToken(),
      csrf.fetchCsrfToken(),
    ])

    expect(fetchMock).toHaveBeenCalledTimes(1)
    expect(tokens).toEqual(['session-token', 'session-token'])
    expect(csrf.getCsrfToken()).toBe('session-token')
  })
})
