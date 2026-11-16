// Runs before every test file. Adds DOM matchers such as toBeInTheDocument()
// and unmounts rendered components after each test so tests can't affect each other.
import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'

afterEach(() => {
  cleanup()
})
