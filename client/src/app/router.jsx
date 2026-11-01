import React, { Suspense, lazy } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from '../features/auth/AuthContext.jsx'
import Loading from '../components/Loading.jsx'
import AppLayout from '../components/AppLayout.jsx'
import ProtectedRoute from '../components/ProtectedRoute.jsx'

const LoginPage = lazy(() => import('../features/auth/LoginPage.jsx'))
const RegisterPage = lazy(() => import('../features/auth/RegisterPage.jsx'))
const TaskList = lazy(() => import('../features/tasks/TaskList.jsx'))
const TaskDetails = lazy(() => import('../features/tasks/TaskDetails.jsx'))
const DashboardPage = lazy(() => import('../features/dashboard/DashboardPage.jsx'))
const AdminPage = lazy(() => import('../features/admin/AdminPage.jsx'))
const NotificationPanel = lazy(() => import('../features/notifications/NotificationPanel.jsx'))

export default function AppRouter() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Suspense fallback={<Loading message="Preparing your workspace..." />}>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<DashboardPage />} />
              <Route path="tasks" element={<TaskList />} />
              <Route path="tasks/:id" element={<TaskDetails />} />
              <Route path="notifications" element={<NotificationPanel />} />
              <Route path="admin" element={<ProtectedRoute requiredRole="admin"><AdminPage /></ProtectedRoute>} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Suspense>
      </AuthProvider>
    </BrowserRouter>
  )
}
