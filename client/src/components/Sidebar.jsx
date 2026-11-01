import React from 'react'
import { NavLink } from 'react-router-dom'
import { useAuth } from '../features/auth/AuthContext.jsx'
import Icon from './Icon.jsx'

const links = [
  { to: '/dashboard', label: 'Overview', icon: 'grid' },
  { to: '/tasks', label: 'My tasks', icon: 'list' },
  { to: '/notifications', label: 'Notifications', icon: 'bell' },
]

export default function Sidebar() {
  const { user } = useAuth()
  const navigation = user?.role === 'admin'
    ? [...links, { to: '/admin', label: 'Administration', icon: 'shield' }]
    : links

  return (
    <aside className="sidebar">
      <div className="brand-lockup">
        <div className="brand-mark"><Icon name="check" size={22} strokeWidth={2.1} /></div>
        <div>
          <p className="brand-wordmark">Task Manager</p>
          <p className="brand-caption">Personal workspace</p>
        </div>
      </div>

      <p className="nav-group-label">Workspace</p>
      <nav className="side-nav" aria-label="Main navigation">
        {navigation.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => `side-nav-link${isActive ? ' active' : ''}`}
          >
            <span className="side-nav-icon"><Icon name={item.icon} size={17} /></span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <strong>Keep your work in view.</strong>
        A clear space to plan, focus, and follow through.
      </div>
    </aside>
  )
}
