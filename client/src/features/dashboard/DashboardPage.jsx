/**
 * DashboardPage component.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S2 (S2-05)
 * Requirement IDs: TMA-F-033
 */

import React, { useState, useEffect } from 'react'
import SummaryCards from './SummaryCards.jsx'
import api from '../../services/api.js'
import Loading from '../../components/Loading.jsx'

export default function DashboardPage() {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function loadSummary() {
      try {
        const res = await api.get('/dashboard/summary')
        if (res.ok && res.data?.success) {
          setSummary(res.data.data)
        } else {
          setError(res.data?.error?.message || 'Failed to load dashboard summary')
        }
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    loadSummary()
  }, [])

  return (
    <div className="container" style={{ padding: '2rem 1rem' }}>
      <h2 style={{ marginBottom: '1.5rem' }}>Dashboard Overview</h2>
      {error && <div className="error-message">{error}</div>}
      {loading ? <Loading message="Loading dashboard..." /> : <SummaryCards summary={summary} />}
    </div>
  )
}

