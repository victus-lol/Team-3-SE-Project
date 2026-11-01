/**
 * API service — base Axios-free fetch wrapper.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-06)
 *
 * All API calls go through this module.
 * CSRF token is injected automatically by csrf.js.
 * Base URL is relative (/api) so the Vite proxy handles routing to Flask.
 */

import { getCsrfToken } from './csrf.js'

const BASE_URL = '/api'

/**
 * Core fetch wrapper.
 * @param {string} path - API path (e.g. '/auth/login')
 * @param {RequestInit} options - fetch options
 * @returns {Promise<{data: any, status: number, ok: boolean}>}
 */
async function request(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  }

  // Inject CSRF token for state-changing methods
  const method = (options.method || 'GET').toUpperCase()
  if (['POST', 'PATCH', 'PUT', 'DELETE'].includes(method)) {
    const csrfToken = getCsrfToken()
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken
    }
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    credentials: 'include', // Always send session cookie
    ...options,
    headers,
  })

  let data = null
  const contentType = response.headers.get('Content-Type') || ''
  if (contentType.includes('application/json')) {
    data = await response.json()
  }

  return { data, status: response.status, ok: response.ok }
}

export const api = {
  get: (path, options = {}) => request(path, { ...options, method: 'GET' }),
  post: (path, body, options = {}) =>
    request(path, { ...options, method: 'POST', body: JSON.stringify(body) }),
  patch: (path, body, options = {}) =>
    request(path, { ...options, method: 'PATCH', body: JSON.stringify(body) }),
  delete: (path, options = {}) => request(path, { ...options, method: 'DELETE' }),
}

export default api

