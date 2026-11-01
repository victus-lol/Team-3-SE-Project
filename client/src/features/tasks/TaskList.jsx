/**
 * TaskList component.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-08), S2 (S2-03)
 * Requirement IDs: TMA-F-010, TMA-F-021
 *
 * TODO checklist (S1-08):
 *   [ ] Fetch and display list of tasks for authenticated user
 *   [ ] Integrate SearchBar and TaskFilters
 *   [ ] Provide button/trigger to open TaskForm for creation
 *   [ ] Handle delete with ConfirmDialog
 */

import React, { useState, useEffect } from 'react'
import taskApi from './taskApi.js'
import TaskCard from './TaskCard.jsx'
import TaskForm from './TaskForm.jsx'
import Loading from '../../components/Loading.jsx'
import ConfirmDialog from '../../components/ConfirmDialog.jsx'

export default function TaskList() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [isFormOpen, setIsFormOpen] = useState(false)
  const [deleteTaskId, setDeleteTaskId] = useState(null)

  const fetchTasks = async () => {
    setLoading(true)
    try {
      const res = await taskApi.getTasks()
      if (res.ok && res.data?.success) {
        setTasks(res.data.data)
      } else {
        setError(res.data?.error?.message || 'Failed to load tasks')
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [])

  const handleDelete = async () => {
    if (!deleteTaskId) return
    try {
      const res = await taskApi.deleteTask(deleteTaskId)
      if (res.ok) {
        setTasks((prev) => prev.filter((t) => t.id !== deleteTaskId))
      }
    } finally {
      setDeleteTaskId(null)
    }
  }

  return (
    <div className="container" style={{ padding: '2rem 1rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2>My Tasks</h2>
        <button className="btn btn-primary" onClick={() => setIsFormOpen(true)}>
          + New Task
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <Loading message="Loading tasks..." />
      ) : tasks.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p className="text-muted">No tasks found. Create your first task to get started!</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '1rem' }}>
          {tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onDelete={(id) => setDeleteTaskId(id)}
              onUpdate={fetchTasks}
            />
          ))}
        </div>
      )}

      {isFormOpen && (
        <TaskForm
          isOpen={isFormOpen}
          onClose={() => setIsFormOpen(false)}
          onSuccess={() => {
            setIsFormOpen(false)
            fetchTasks()
          }}
        />
      )}

      <ConfirmDialog
        isOpen={Boolean(deleteTaskId)}
        title="Delete Task"
        message="Are you sure you want to delete this task? This action cannot be undone."
        onConfirm={handleDelete}
        onCancel={() => setDeleteTaskId(null)}
      />
    </div>
  )
}

