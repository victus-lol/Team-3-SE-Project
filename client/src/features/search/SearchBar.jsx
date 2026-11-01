/**
 * SearchBar component.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S2 (S2-03)
 * Requirement IDs: TMA-F-021
 */

import React, { useState } from 'react'

export default function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('')

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      onSearch(query)
    }
  }

  return (
    <div style={{ display: 'flex', gap: '0.5rem', width: '100%' }}>
      <input
        type="search"
        placeholder="Search tasks by title or description..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        style={{ flex: 1, padding: '0.5rem', border: '1px solid var(--color-border)', borderRadius: 'var(--radius)' }}
      />
      <button className="btn btn-primary" onClick={() => onSearch(query)}>
        Search
      </button>
    </div>
  )
}

