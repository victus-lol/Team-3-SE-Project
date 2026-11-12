/**
 * Authentication API client.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-07)
 * Requirement IDs: TMA-F-001, TMA-F-002
 */

import api from '../../services/api.js'

export const authApi = {
  login: (credentials) => api.post('/auth/login', credentials),
  logout: () => api.post('/auth/logout', {}),
  getMe: () => api.get('/auth/me'),
  register: (userData) => api.post('/auth/register', userData),
  requestPasswordReset: (email) => api.post('/auth/password-reset/request', { email }),
  confirmPasswordReset: (token, password) => api.post('/auth/password-reset/confirm', { token, password }),
  getCsrf: () => api.get('/auth/csrf'),
}

export default authApi

