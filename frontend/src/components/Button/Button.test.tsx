import React from 'react';
import { fireEvent, render } from '@testing-library/react';
import Button from './Button';
import { describe, expect, it, vi } from 'vitest';

describe('Button component', () => {

    it('renders correctly', () => {
        const mockOnClick = vi.fn();
        const { getByText } = render(<Button title="Test Button" onClick={mockOnClick} />);
        const buttonElement = getByText('Test Button');

        expect(document.body.contains(buttonElement)).toBe(true);
    });

    it('calls onClick handler only once', () => {
        const mockOnClick = vi.fn();
        const { getByText } = render(<Button title="Test Button" onClick={mockOnClick} />);

        const button = getByText('Test Button');
        fireEvent.click(button);
        fireEvent.click(button); // second click

        expect(mockOnClick).toHaveBeenCalledTimes(1);
    });

    it('does not call onClick when disabled is true', () => {
        const mockOnClick = vi.fn();
        const { getByText } = render(<Button title="Test Button" onClick={mockOnClick} disabled={true} />);

        const button = getByText('Test Button');
        fireEvent.click(button);

        expect(mockOnClick).not.toHaveBeenCalled();
    });

    it('applies custom class and style', () => {
        const mockOnClick = vi.fn();
        const style = { backgroundColor: 'blue' };
        const { getByText } = render(<Button title="Test Button" className="custom-class" style={style} onClick={mockOnClick} />);

        const button = getByText('Test Button');
        
        expect(button.classList.contains('custom-class')).toBe(true);
        expect(button.style.backgroundColor).toBe('blue');
    });

});
