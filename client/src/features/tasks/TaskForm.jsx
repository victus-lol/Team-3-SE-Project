import React, { useRef, useState } from 'react'
import taskApi from './taskApi.js'
import Icon from '../../components/Icon.jsx'
import useDialogAccessibility from '../../hooks/useDialogAccessibility.js'

export default function TaskForm({ isOpen, onClose, onSuccess, initialData = null }) {
  const [title, setTitle] = useState(initialData?.title || '')
  const [description, setDescription] = useState(initialData?.description || '')
  const [priority, setPriority] = useState(initialData?.priority || 'medium')
  const [status, setStatus] = useState(initialData?.status || 'pending')
  const [dueDate, setDueDate] = useState(initialData?.due_date || '')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const dialogRef = useRef(null)
  useDialogAccessibility(dialogRef, isOpen, submitting ? undefined : onClose)

  if (!isOpen) return null

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setSubmitting(true)

    const payload = { title: title.trim(), description: description.trim() || null, priority, status, due_date: dueDate || null }
    try {
      const res = initialData?.id
        ? await taskApi.updateTask(initialData.id, payload)
        : await taskApi.createTask(payload)

      if (res.ok && res.data?.success) {
        onSuccess()
      } else {
        setError(res.data?.error?.message || 'The task could not be saved.')
      }
    } catch (err) {
      setError(err.message || 'Could not reach the task service.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="modal-backdrop" onMouseDown={(event) => { if (event.target === event.currentTarget && !submitting) onClose() }}>
      <section ref={dialogRef} className="modal-card" role="dialog" aria-modal="true" aria-labelledby="task-form-title" tabIndex="-1">
        <div className="modal-header">
          <div>
            <p className="eyebrow">Task details</p>
            <h2 id="task-form-title">{initialData ? 'Edit task' : 'Create a task'}</h2>
            <p>Keep the outcome and next step easy to understand.</p>
          </div>
          <button className="icon-button" type="button" aria-label="Close dialog" onClick={onClose} disabled={submitting}><Icon name="close" size={16} /></button>
        </div>
        {error && <div className="error-message" role="alert">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-field">
              <label htmlFor="task-title">Task title <span aria-hidden="true">*</span></label>
              <input id="task-title" name="title" type="text" value={title} onChange={(event) => setTitle(event.target.value)} maxLength={200} required data-dialog-autofocus />
            </div>
            <div className="form-field">
              <label htmlFor="task-description">Description</label>
              <textarea id="task-description" name="description" value={description} onChange={(event) => setDescription(event.target.value)} maxLength={2000} placeholder="Add helpful context or a next step" />
            </div>
            <div className="form-row">
              <div className="form-field">
                <label htmlFor="task-priority">Priority</label>
                <select id="task-priority" value={priority} onChange={(event) => setPriority(event.target.value)}>
                  <option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option>
                </select>
              </div>
              <div className="form-field">
                <label htmlFor="task-status">Status</label>
                <select id="task-status" value={status} onChange={(event) => setStatus(event.target.value)}>
                  <option value="pending">To do</option><option value="in_progress">In progress</option><option value="completed">Completed</option>
                </select>
              </div>
            </div>
            <div className="form-field">
              <label htmlFor="task-due-date">Due date</label>
              <input id="task-due-date" type="date" value={dueDate} onChange={(event) => setDueDate(event.target.value)} />
            </div>
          </div>
          <div className="modal-actions">
            <button className="btn btn-quiet" type="button" onClick={onClose} disabled={submitting}>Cancel</button>
            <button className="btn btn-primary" type="submit" disabled={submitting || !title.trim()}>
              {submitting ? 'Saving…' : <><Icon name="check" size={15} /> {initialData ? 'Save changes' : 'Create task'}</>}
            </button>
          </div>
        </form>
      </section>
    </div>
  )
}
