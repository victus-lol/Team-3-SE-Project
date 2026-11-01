import React, { useCallback, useEffect, useMemo, useState } from 'react'
import taskApi from './taskApi.js'
import TaskCard from './TaskCard.jsx'
import TaskForm from './TaskForm.jsx'
import Loading from '../../components/Loading.jsx'
import ConfirmDialog from '../../components/ConfirmDialog.jsx'
import SearchBar from '../search/SearchBar.jsx'
import TaskFilters from '../search/TaskFilters.jsx'
import Icon from '../../components/Icon.jsx'

export default function TaskList() {
  const [tasks, setTasks] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [isFormOpen, setIsFormOpen] = useState(false)
  const [activeTask, setActiveTask] = useState(null)
  const [deleteTask, setDeleteTask] = useState(null)
  const [deleteError, setDeleteError] = useState('')
  const [query, setQuery] = useState('')
  const [filters, setFilters] = useState({ status: '', priority: '', overdue: false })

  const fetchTasks = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const res = await taskApi.getTasks()
      if (res.ok && res.data?.success && Array.isArray(res.data.data)) {
        setTasks(res.data.data)
      } else {
        setTasks(null)
        setError(res.data?.error?.message || 'Task service is not available yet.')
      }
    } catch (err) {
      setTasks(null)
      setError(err.message || 'Could not reach the task service.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchTasks() }, [fetchTasks])

  const visibleTasks = useMemo(() => {
    if (!tasks) return []
    const currentDate = new Date()
    const today = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(currentDate.getDate()).padStart(2, '0')}`
    return tasks.filter((task) => {
      const normalizedQuery = query.trim().toLowerCase()
      const matchesQuery = !normalizedQuery || `${task.title || ''} ${task.description || ''}`.toLowerCase().includes(normalizedQuery)
      const matchesStatus = !filters.status || task.status === filters.status
      const matchesPriority = !filters.priority || task.priority === filters.priority
      const overdue = task.due_date && task.due_date < today && task.status !== 'completed'
      return matchesQuery && matchesStatus && matchesPriority && (!filters.overdue || overdue)
    })
  }, [tasks, query, filters])

  const handleDelete = async () => {
    if (!deleteTask) return
    setDeleteError('')
    try {
      const res = await taskApi.deleteTask(deleteTask.id)
      if (res.ok) {
        setTasks((current) => current?.filter((task) => task.id !== deleteTask.id) ?? null)
        setDeleteTask(null)
      } else {
        setDeleteError(res.data?.error?.message || 'The task could not be deleted.')
      }
    } catch (err) {
      setDeleteError(err.message || 'Could not reach the task service.')
    }
  }

  const openCreate = () => { setActiveTask(null); setIsFormOpen(true) }
  const openEdit = (task) => { setActiveTask(task); setIsFormOpen(true) }
  const closeForm = () => { setIsFormOpen(false); setActiveTask(null) }

  return (
    <>
      <div className="page-heading">
        <div>
          <p className="eyebrow">Workspace / Tasks</p>
          <h1 className="page-title">My tasks</h1>
          <p className="page-subtitle">Keep the next step clear and the important work moving.</p>
        </div>
        <button className="btn btn-primary" type="button" onClick={openCreate}><Icon name="plus" size={16} /> Create task</button>
      </div>

      <div className="task-toolbar">
        <SearchBar onSearch={setQuery} />
        <TaskFilters filters={filters} onChange={setFilters} />
      </div>

      <div className="section-heading" style={{ marginTop: 18 }}>
        <div><h2>{loading ? 'Loading tasks' : tasks ? `${visibleTasks.length} ${visibleTasks.length === 1 ? 'task' : 'tasks'}` : 'Task list'}</h2><p>Sorted by your current filters</p></div>
        {tasks && <span className="eyebrow" style={{ margin: 0 }}>{tasks.filter((task) => task.status !== 'completed').length} open</span>}
      </div>

      {error && <div className="notice" role="status">{error} The task API in this local project is still awaiting implementation.</div>}
      {deleteError && <div className="error-message" role="alert">{deleteError}</div>}
      {loading ? <Loading message="Loading your tasks..." /> : tasks === null ? (
        <div className="card empty-state"><Icon name="list" size={23} /><strong>Your task list will appear here</strong><p>Once the task service is connected, you can create and manage work from this page.</p></div>
      ) : visibleTasks.length ? (
        <div className="task-list">
          {visibleTasks.map((task) => <TaskCard key={task.id} task={task} onEdit={openEdit} onDelete={() => setDeleteTask(task)} />)}
        </div>
      ) : (
        <div className="card empty-state"><Icon name="search" size={22} /><strong>{tasks.length ? 'No tasks match those filters' : 'A clear slate'}</strong><p>{tasks.length ? 'Try a different search or reset one of the filters.' : 'Create your first task when you’re ready to get started.'}</p>{!tasks.length && <button className="btn btn-primary" style={{ marginTop: 14 }} onClick={openCreate}><Icon name="plus" size={15} /> Create task</button>}</div>
      )}

      {isFormOpen && <TaskForm key={activeTask?.id || 'new'} isOpen={isFormOpen} initialData={activeTask} onClose={closeForm} onSuccess={() => { closeForm(); fetchTasks() }} />}

      <ConfirmDialog
        isOpen={Boolean(deleteTask)}
        title="Delete this task?"
        message={deleteError || (deleteTask ? `“${deleteTask.title}” will be permanently removed from your task list.` : '')}
        confirmText="Delete task"
        onConfirm={handleDelete}
        onCancel={() => { setDeleteTask(null); setDeleteError('') }}
      />
    </>
  )
}
