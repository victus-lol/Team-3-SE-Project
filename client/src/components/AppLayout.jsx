import React from 'react'
import { Outlet } from 'react-router-dom'
import Navbar from './Navbar.jsx'
import Sidebar from './Sidebar.jsx'

export default function AppLayout() {
  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">Skip to main content</a>
      <Sidebar />
      <div className="app-main">
        <Navbar />
        <main id="main-content" className="page-content" tabIndex="-1">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
