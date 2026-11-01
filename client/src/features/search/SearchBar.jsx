import React, { useState } from 'react'
import Icon from '../../components/Icon.jsx'

export default function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('')

  const submit = (event) => {
    event.preventDefault()
    onSearch(query)
  }

  return (
    <form className="search-control" role="search" onSubmit={submit}>
      <Icon name="search" size={16} />
      <input
        type="search"
        aria-label="Search tasks"
        placeholder="Search tasks by title or description"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
      />
    </form>
  )
}
