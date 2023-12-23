import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import AppBar from './AppBar';
import { BrowserRouter as Router } from 'react-router-dom';

describe('AppBar', () => {

  const BASE_URL = 'https://www.amsterdammusiclab.nl';

  beforeEach(() => {
    jest.resetModules();
    import.meta.env.VITE_AML_HOME = BASE_URL;
  });

  it('renders correctly', () => {
    const { getByText } = render(<AppBar title="Test Title" />, { wrapper: Router });
    expect(getByText('Test Title')).toBeInTheDocument();
  });

  it('renders logo as Link for relative URL', () => {
    const { getByLabelText } = render(<AppBar title="Test Title" />, { wrapper: Router });
    const logo = getByLabelText('Logo');
    expect(logo.tagName).toBe('A');
    expect(logo.getAttribute('href')).toBe(BASE_URL);
  });

  it('renders logo as an a-element for absolute URL', () => {
    const { getByLabelText } = render(<AppBar title="Test Title" />, { wrapper: Router });
    const logo = getByLabelText('Logo');
    expect(logo.tagName).toBe('A');
    expect(logo.getAttribute('href')).toBe(BASE_URL);
  });

  it('prevents navigation when logoClickConfirm is provided and user cancels', () => {
    // Mock window.confirm
    window.confirm = jest.fn(() => false);

    const { getByLabelText } = render(<AppBar title="Test Title" logoClickConfirm="Confirm?" />, { wrapper: Router });
    const logo = getByLabelText('Logo');
    fireEvent.click(logo);

    expect(window.confirm).toHaveBeenCalledWith('Confirm?');
  });

});
