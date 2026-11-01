/**
 * Frontend Foundation tests.
 * Owner: Aaryan Dubey (PES2UG24CS016)
 * Sprint: S1 (S1-06)
 */

import React from 'react'
import { render, screen } from '@testing-library/react'
import Loading from '../components/Loading.jsx'
import App from '../app/App.jsx'

describe('Frontend Foundation', () => {
  it('renders Loading spinner component with default message', () => {
    render(<Loading />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('renders Loading spinner with custom message', () => {
    render(<Loading message="Custom waiting..." />)
    expect(screen.getByText('Custom waiting...')).toBeInTheDocument()
  })

  it('renders App shell without crashing', () => {
    render(<App />)
    expect(screen.getByText('Task Manager')).toBeInTheDocument()
  })
})

