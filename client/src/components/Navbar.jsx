import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../features/auth/AuthContext.jsx'
import Icon from './Icon.jsx'

function initials(name = 'User') {
  return name.split(/\s+/).filter(Boolean).slice(0, 2).map((part) => part[0]).join('').toUpperCase()
}

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    try {
      await logout()
    } finally {
      navigate('/login', { replace: true })
    }
  }

  return (
    <header className="topbar">
      <div className="topbar-context">Workspace <span aria-hidden="true">/</span> Personal</div>
      <div className="topbar-user">
        <div className="avatar" aria-hidden="true">{initials(user?.name || user?.email)}</div>
        <div className="user-meta">
          <strong>{user?.name || user?.email || 'Workspace member'}</strong>
          <span>{user?.role || 'Member'}</span>
        </div>
        <button className="logout-button" type="button" onClick={handleLogout}>
          <Icon name="logout" size={15} />
          <span>Sign out</span>
        </button>
      </div>
    </header>
  )
}
