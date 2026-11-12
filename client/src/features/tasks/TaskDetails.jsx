import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import taskApi from './taskApi.js'
import Loading from '../../components/Loading.jsx'
import Icon from '../../components/Icon.jsx'

export default function TaskDetails() {
  const { id } = useParams()
  const [task, setTask] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    async function load() {
      try {
        const res = await taskApi.getTask(id)
        if (!active) return
        if (res.ok && res.data?.success) setTask(res.data.data)
        else setError(res.data?.error?.message || 'Task details are not available.')
      } catch (err) {
        if (active) setError(err.message || 'Could not reach the task service.')
      } finally {
        if (active) setLoading(false)
      }
    }
    load()
    return () => { active = false }
  }, [id])

  if (loading) return <Loading message="Loading task details..." />

  return (
    <>
      <p className="eyebrow">Workspace / Tasks / Details</p>
      <p style={{ marginBottom: 18 }}><Link className="text-link" to="/tasks"><Icon name="arrow" size={13} style={{ transform: 'rotate(180deg)', verticalAlign: 'middle' }} /> Back to tasks</Link></p>
      {error ? <div className="notice" role="alert">{error}</div> : task && (
        <article className="card task-detail-card">
          <div className="page-heading" style={{ marginBottom: 12 }}>
            <div><h1 className="page-title">{task.title}</h1><p className="page-subtitle">Task #{task.id}</p></div>
            <span className={`pill status-${task.status}`}>{(task.status || 'pending').replace('_', ' ')}</span>
          </div>
          <p className="muted">{task.description || 'No description provided.'}</p>
          <div className="task-detail-grid">
            <div><span>Priority</span><strong>{task.priority || 'Medium'}</strong></div>
            <div><span>Status</span><strong>{(task.status || 'pending').replace('_', ' ')}</strong></div>
            <div><span>Due date</span><strong>{task.due_date || 'Not set'}</strong></div>
          </div>
        </article>
      )}
    </>
  )
}
