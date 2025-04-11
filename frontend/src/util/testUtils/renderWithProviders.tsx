import { ReactNode } from 'react'
import { render, RenderOptions } from '@testing-library/react'
import { ThemeProvider } from '@/theme/ThemeProvider'

const Providers = ({ children }: { children: ReactNode }) => {
  // Add other providers if needed
  return <ThemeProvider>{children}</ThemeProvider>
}

export const renderWithProviders = (
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) =>
  render(ui, {
    wrapper: Providers,
    ...options,
  })
