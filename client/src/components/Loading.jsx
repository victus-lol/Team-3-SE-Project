import React from 'react'

export default function Loading({ message = 'Loading...' }) {
  return (
    <div className="loading-wrap" role="status" aria-live="polite">
      <span className="brand-wordmark">Task Manager</span>
      <span className="loading-spinner" aria-hidden="true" />
      <span>{message}</span>
    </div>
  )
}
