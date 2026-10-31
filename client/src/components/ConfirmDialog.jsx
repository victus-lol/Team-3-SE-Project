/**
 * ConfirmDialog component.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-08)
 * Requirement IDs: TMA-F-012
 *
 * TODO checklist:
 *   [ ] Implement modal dialog for destructive actions (e.g. task delete)
 *   [ ] Support title, message, confirmText, cancelText, onConfirm, onCancel
 */

import React from 'react'

export default function ConfirmDialog({ isOpen, title, message, onConfirm, onCancel }) {
  if (!isOpen) return null

  return (
    <div style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex',
      alignItems: 'center', justifyContent: 'center', zIndex: 1000
    }}>
      <div className="card" style={{ maxWidth: '400px', width: '100%', margin: '1rem' }}>
        <h3 style={{ marginBottom: '0.5rem' }}>{title || 'Confirm Action'}</h3>
        <p className="text-muted" style={{ marginBottom: '1.5rem' }}>{message || 'Are you sure?'}</p>
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
          <button className="btn" onClick={onCancel}>Cancel</button>
          <button className="btn btn-danger" onClick={onConfirm}>Confirm</button>
        </div>
      </div>
    </div>
  )
}

