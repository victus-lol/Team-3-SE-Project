import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'
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
  const requestVersionRef = useRef(0)
  const criteria = useMemo(() => ({
    q: query.trim(),
    status: filters.status,
    priority: filters.priority,
    overdue: filters.overdue ? 'true' : '',
  }), [query, filters])

  const fetchTasks = useCallback(async (criteria = {}) => {
    const requestId = ++requestVersionRef.current
    setLoading(true)
    setError('')
    try {
      const res = await taskApi.getTasks(criteria)
      if (requestId !== requestVersionRef.current) return
      if (res.ok && res.data?.success && Array.isArray(res.data.data)) {
        setTasks(res.data.data)
      } else {
        setTasks(null)
        setError(res.data?.error?.message || 'The task list could not be loaded.')
      }
    } catch (err) {
      if (requestId !== requestVersionRef.current) return
      setTasks(null)
      setError(err.message || 'Could not reach the task service.')
    } finally {
      if (requestId === requestVersionRef.current) setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchTasks(criteria)
  }, [fetchTasks, criteria])

  const visibleTasks = tasks || []

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
        <div><h2>{loading ? 'Loading tasks' : tasks ? `${visibleTasks.length} ${visibleTasks.length === 1 ? 'task' : 'tasks'}` : 'Task list'}</h2><p>Results for your search and filters</p></div>
        {tasks && <span className="eyebrow" style={{ margin: 0 }}>{tasks.filter((task) => task.status !== 'completed').length} open</span>}
      </div>

      {error && <div className="notice" role="alert">{error} <button className="text-link" type="button" onClick={() => fetchTasks(criteria)}>Try again</button></div>}
      {deleteError && <div className="error-message" role="alert">{deleteError}</div>}
      {loading ? <Loading message="Loading your tasks..." /> : tasks === null ? (
        <div className="card empty-state"><Icon name="list" size={23} /><strong>Tasks could not be loaded</strong><p>Check your connection and use the retry control above.</p></div>
      ) : visibleTasks.length ? (
        <div className="task-list">
          {visibleTasks.map((task) => <TaskCard key={task.id} task={task} onEdit={openEdit} onDelete={() => setDeleteTask(task)} />)}
        </div>
      ) : (
        <div className="card empty-state"><Icon name="search" size={22} /><strong>{query || filters.status || filters.priority || filters.overdue ? 'No tasks match those filters' : 'A clear slate'}</strong><p>{query || filters.status || filters.priority || filters.overdue ? 'Try a different search or reset one of the filters.' : 'Create your first task when you’re ready to get started.'}</p>{!(query || filters.status || filters.priority || filters.overdue) && <button className="btn btn-primary" style={{ marginTop: 14 }} onClick={openCreate}><Icon name="plus" size={15} /> Create task</button>}</div>
      )}

      {isFormOpen && <TaskForm key={activeTask?.id || 'new'} isOpen={isFormOpen} initialData={activeTask} onClose={closeForm} onSuccess={() => { closeForm(); fetchTasks(criteria) }} />}

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
