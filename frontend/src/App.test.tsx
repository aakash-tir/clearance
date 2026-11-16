import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import App from './App'

describe('App shell', () => {
  it('shows the product name as the main heading', () => {
    render(<App />)

    // getByRole finds elements the way a screen reader would, so this also checks
    // the heading is a real <h1>, not just big text.
    expect(screen.getByRole('heading', { level: 1, name: 'Clearance' })).toBeInTheDocument()
  })

  it('tells the user that answers are limited to what they can access', () => {
    render(<App />)

    expect(screen.getByText(/only get answers from what you're allowed to see/i)).toBeInTheDocument()
  })
})
