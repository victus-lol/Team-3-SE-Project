/**
 * CSRF token management.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-06)
 *
 * Fetches the CSRF token from GET /api/auth/csrf and stores it in memory.
 * NEVER stores session identifiers or tokens in localStorage.
 * The token is kept in module scope (memory only).
 */

let _csrfToken = null

/**
 * Fetch and store the CSRF token from the backend.
 * Call this once on app startup (in AuthProvider).
 */
export async function fetchCsrfToken() {
  try {
    const response = await fetch('/api/auth/csrf', {
      method: 'GET',
      credentials: 'include',
    })
    if (response.ok) {
      const data = await response.json()
      _csrfToken = data?.data?.csrf_token || null
    }
  } catch (err) {
    // Non-fatal: CSRF token will be null; protected routes will fail gracefully
    console.warn('Failed to fetch CSRF token:', err)
  }
}

/** Get the currently stored CSRF token. */
export function getCsrfToken() {
  return _csrfToken
}

/** Clear the stored token (e.g. after logout). */
export function clearCsrfToken() {
  _csrfToken = null
}

