/**
 * TaskDetails component.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-08)
 * Requirement IDs: TMA-F-010
 */

import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import taskApi from './taskApi.js'
import Loading from '../../components/Loading.jsx'

export default function TaskDetails() {
  const { id } = useParams()
  const [task, setTask] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const res = await taskApi.getTask(id)
        if (res.ok && res.data?.success) {
          setTask(res.data.data)
        } else {
          setError(res.data?.error?.message || 'Task not found')
        }
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [id])

  if (loading) return <Loading />
  if (error) return <div className="container error-message">{error}</div>

  return (
    <div className="container" style={{ padding: '2rem 1rem', maxWidth: '600px' }}>
      <Link to="/tasks" style={{ display: 'inline-block', marginBottom: '1rem' }}>&larr; Back to Tasks</Link>
      <div className="card">
        <h2>{task.title}</h2>
        <p className="text-muted" style={{ margin: '1rem 0' }}>{task.description || 'No description provided.'}</p>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', borderTop: '1px solid var(--color-border)', paddingTop: '1rem' }}>
          <div><strong>Priority:</strong> {task.priority}</div>
          <div><strong>Status:</strong> {task.status}</div>
          <div><strong>Due Date:</strong> {task.due_date || 'None'}</div>
        </div>
      </div>
    </div>
  )
}

