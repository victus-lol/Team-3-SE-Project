import React, { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext.jsx'
import SummaryCards from './SummaryCards.jsx'
import taskApi from '../tasks/taskApi.js'
import api from '../../services/api.js'
import Loading from '../../components/Loading.jsx'
import Icon from '../../components/Icon.jsx'

function taskCounts(tasks) {
  return tasks.reduce((counts, task) => {
    if (Object.hasOwn(counts, task.status)) counts[task.status] += 1
    return counts
  }, { pending: 0, in_progress: 0, completed: 0 })
}

function dueLabel(value) {
  if (!value) return 'No due date'
  const date = new Date(`${value}T00:00:00`)
  return Number.isNaN(date.valueOf()) ? `Due ${value}` : `Due ${new Intl.DateTimeFormat('en', { month: 'short', day: 'numeric' }).format(date)}`
}

export default function DashboardPage() {
  const { user } = useAuth()
  const [summary, setSummary] = useState(null)
  const [tasks, setTasks] = useState(null)
  const [loading, setLoading] = useState(true)
  const [summaryError, setSummaryError] = useState('')
  const [tasksError, setTasksError] = useState('')

  useEffect(() => {
    let active = true
    async function loadDashboard() {
      const [summaryResult, tasksResult] = await Promise.allSettled([
        api.get('/dashboard/summary'),
        taskApi.getTasks(),
      ])

      if (!active) return
      if (summaryResult.status === 'fulfilled' && summaryResult.value.ok && summaryResult.value.data?.success) {
        setSummary(summaryResult.value.data.data)
      } else {
        const message = summaryResult.status === 'rejected'
          ? summaryResult.reason?.message
          : summaryResult.value?.data?.error?.message
        setSummaryError(message || 'Summary data could not be loaded.')
      }
      if (tasksResult.status === 'fulfilled' && tasksResult.value.ok && tasksResult.value.data?.success) {
        setTasks(Array.isArray(tasksResult.value.data.data) ? tasksResult.value.data.data : [])
      } else {
        const message = tasksResult.status === 'rejected'
          ? tasksResult.reason?.message
          : tasksResult.value?.data?.error?.message
        setTasksError(message || 'Task data could not be loaded.')
      }
      setLoading(false)
    }
    loadDashboard()
    return () => { active = false }
  }, [])

  const counts = useMemo(() => summary || (tasks ? taskCounts(tasks) : null), [summary, tasks])
  const now = new Date()
  const hour = now.getHours()
  const greeting = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening'
  const dateLabel = new Intl.DateTimeFormat('en', { weekday: 'long', month: 'long', day: 'numeric' }).format(now)
  const firstName = user?.name?.trim().split(/\s+/)[0] || 'there'
  const upcomingTasks = tasks ? tasks.filter((task) => task.status !== 'completed').slice(0, 4) : []

  return (
    <>
      <section className="dashboard-hero">
        <div className="hero-copy">
          <p className="eyebrow">Your workspace</p>
          <h1 className="hero-title">{greeting}, {firstName}.</h1>
          <p className="hero-description">A little structure makes room for your best work. Here’s what’s happening with your tasks.</p>
        </div>
        <div className="hero-side">
          <span className="hero-date">{dateLabel}</span>
          <Link className="btn" to="/tasks"><Icon name="plus" size={15} /> New task</Link>
        </div>
      </section>

      {loading ? <Loading message="Loading your workspace..." /> : (
        <>
          {tasksError && <div className="notice" role="status">Task data is currently unavailable from the API. {tasksError}</div>}
          <div className="section-heading">
            <div><h2>At a glance</h2><p>Progress across your current workload</p></div>
            <span className="eyebrow" style={{ margin: 0 }}>Overview</span>
          </div>
          <SummaryCards summary={counts} />
          {summaryError && !tasks && <p className="muted" style={{ marginTop: 10, fontSize: 10 }}>{summaryError}</p>}

          <div className="dashboard-lower">
            <section className="card panel" aria-labelledby="upcoming-heading">
              <div className="panel-heading">
                <div><h2 id="upcoming-heading">In focus</h2><p>Your next open tasks</p></div>
                <Link className="text-link" to="/tasks">View all</Link>
              </div>
              {tasks === null ? (
                <div className="empty-state"><Icon name="list" size={21} /><strong>Task data could not be loaded</strong><p>{tasksError || 'Try again after checking your connection.'}</p></div>
              ) : upcomingTasks.length ? (
                <div className="task-preview-list">
                  {upcomingTasks.map((task) => (
                    <Link className="task-preview" to={`/tasks/${task.id}`} key={task.id}>
                      <span className={`task-dot ${task.status}`} />
                      <span className="task-preview-copy"><strong>{task.title}</strong><span>{task.priority || 'Standard'} priority</span></span>
                      <span className="task-preview-date">{dueLabel(task.due_date)}</span>
                    </Link>
                  ))}
                </div>
              ) : (
                <div className="empty-state"><Icon name="check" size={21} /><strong>You’re all caught up</strong><p>New tasks you create will appear here.</p></div>
              )}
            </section>

            <aside className="focus-card">
              <p className="focus-kicker">A thoughtful workflow</p>
              <h3>Make progress visible.</h3>
              <p>Keep priorities clear, give each task a next step, and come back to your plan as work changes.</p>
              <Link className="text-link" to="/tasks">Open your task list <Icon name="arrow" size={13} style={{ verticalAlign: 'middle' }} /></Link>
            </aside>
          </div>
        </>
      )}
    </>
  )
}
