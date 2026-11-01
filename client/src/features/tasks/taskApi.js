/**
 * Task API client.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-08)
 * Requirement IDs: TMA-F-010, TMA-F-011, TMA-F-012, TMA-F-021
 */

import api from '../../services/api.js'

export const taskApi = {
  getTasks: (params = {}) => {
    const query = new URLSearchParams()
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        query.append(key, value)
      }
    })
    const qs = query.toString()
    return api.get(`/tasks${qs ? `?${qs}` : ''}`)
  },
  getTask: (id) => api.get(`/tasks/${id}`),
  createTask: (taskData) => api.post('/tasks', taskData),
  updateTask: (id, taskData) => api.patch(`/tasks/${id}`, taskData),
  deleteTask: (id) => api.delete(`/tasks/${id}`),
}

export default taskApi

