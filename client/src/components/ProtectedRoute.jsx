/**
 * ProtectedRoute component.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-07)
 * Requirement IDs: TMA-F-001, TMA-SR-001
 *
 * Checks if user is authenticated; redirects to /login if not.
 * Supports role checking (e.g. requiredRole='admin').
 *
 * TODO checklist:
 *   [ ] Integrate with AuthContext
 *   [ ] Render Loading while auth status is unknown
 *   [ ] Redirect to /login with state={{ from: location }}
 *   [ ] Support admin role check redirecting to 403 or home
 */

import React from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../features/auth/AuthContext.jsx'
import Loading from './Loading.jsx'

export default function ProtectedRoute({ children, requiredRole }) {
  const { user, loading } = useAuth()
  const location = useLocation()

  if (loading) {
    return <Loading message="Checking authentication..." />
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to="/" replace />
  }

  return children
}

