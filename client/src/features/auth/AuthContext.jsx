/**
 * AuthContext — global authentication state provider.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-07)
 * Requirement IDs: TMA-F-001, TMA-F-002, TMA-SR-001
 *
 * Stores user session state in memory (never localStorage).
 * Handles login, logout, and checking session via /api/auth/me on load.
 * Fetches CSRF token on initialization.
 *
 */

import React, { createContext, useContext, useState, useEffect } from 'react'
import authApi from './authApi.js'
import { fetchCsrfToken, clearCsrfToken } from '../../services/csrf.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function initAuth() {
      try {
        await fetchCsrfToken()
        const res = await authApi.getMe()
        if (res.ok && res.data?.success) {
          setUser(res.data.data)
        } else {
          setUser(null)
        }
      } catch {
        setUser(null)
      } finally {
        setLoading(false)
      }
    }
    initAuth()
  }, [])

  const login = async (email, password) => {
    setError(null)
    const res = await authApi.login({ email, password })
    if (res.ok && res.data?.success) {
      setUser(res.data.data)
      return { success: true }
    } else {
      const msg = res.data?.error?.message || 'Login failed'
      setError(msg)
      return { success: false, error: msg }
    }
  }

  const logout = async () => {
    try {
      await authApi.logout()
    } finally {
      setUser(null)
      clearCsrfToken()
    }
  }

  return (
    <AuthContext.Provider value={{ user, loading, error, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

