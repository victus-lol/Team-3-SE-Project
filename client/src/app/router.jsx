/**
 * Application router — defines all routes.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-06, S1-07)
 * Requirement IDs: TMA-F-001, TMA-F-002, TMA-F-010
 *
 * TODO checklist (S1-06, S1-07):
 *   [ ] Add protected route wrapper (ProtectedRoute)
 *   [ ] Implement route for /login
 *   [ ] Implement route for /register (scope-pending)
 *   [ ] Implement route for /tasks (task list)
 *   [ ] Implement route for /tasks/:id (task details)
 *   [ ] Implement route for /dashboard
 *   [ ] Implement route for /admin (admin guard)
 *   [ ] Redirect unauthenticated users to /login
 */

import React, { Suspense, lazy } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from '../features/auth/AuthContext.jsx'
import Loading from '../components/Loading.jsx'
import HealthStatus from '../components/HealthStatus.jsx'

// Lazy-loaded feature pages (skeletons — to be implemented)
const LoginPage = lazy(() => import('../features/auth/LoginPage.jsx'))
const RegisterPage = lazy(() => import('../features/auth/RegisterPage.jsx'))
const TaskList = lazy(() => import('../features/tasks/TaskList.jsx'))
const DashboardPage = lazy(() => import('../features/dashboard/DashboardPage.jsx'))
const AdminPage = lazy(() => import('../features/admin/AdminPage.jsx'))

export default function AppRouter() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Suspense fallback={<Loading />}>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            {/* App shell / home — shows API status */}
            <Route path="/" element={<HealthStatus />} />

            {/* Protected routes (ProtectedRoute wrapper — TODO S1-07) */}
            <Route path="/tasks" element={<TaskList />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/admin" element={<AdminPage />} />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Suspense>
      </AuthProvider>
    </BrowserRouter>
  )
}

