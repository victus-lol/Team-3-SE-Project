import React, { useRef, useState } from 'react'
import useDialogAccessibility from '../hooks/useDialogAccessibility.js'

export default function ConfirmDialog({ isOpen, title, message, confirmText = 'Confirm', onConfirm, onCancel }) {
  const [working, setWorking] = useState(false)
  const dialogRef = useRef(null)
  useDialogAccessibility(dialogRef, isOpen, working ? undefined : onCancel)
  if (!isOpen) return null

  const confirm = async () => {
    setWorking(true)
    try { await onConfirm?.() } finally { setWorking(false) }
  }

  return (
    <div className="modal-backdrop" onMouseDown={(event) => { if (event.target === event.currentTarget && !working) onCancel?.() }}>
      <section ref={dialogRef} className="modal-card" role="alertdialog" aria-modal="true" aria-labelledby="confirm-dialog-title" aria-describedby="confirm-dialog-message" style={{ maxWidth: 430 }} tabIndex="-1">
        <div className="modal-header">
          <div><p className="eyebrow">Please confirm</p><h2 id="confirm-dialog-title">{title || 'Confirm action'}</h2><p id="confirm-dialog-message">{message || 'Are you sure you want to continue?'}</p></div>
        </div>
        <div className="modal-actions">
          <button className="btn btn-quiet" type="button" onClick={onCancel} disabled={working}>Cancel</button>
          <button className="btn btn-danger" type="button" onClick={confirm} disabled={working}>{working ? 'Working…' : confirmText}</button>
        </div>
      </section>
    </div>
  )
}
