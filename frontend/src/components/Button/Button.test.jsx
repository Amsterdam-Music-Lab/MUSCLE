import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import Button from './Button';
import { vi } from 'vitest';

describe('Button component', () => {

    it('renders correctly', () => {
        render(<Button title="Test Button" />);
        const buttonElement = screen.getByText('Test Button');
        expect(document.body.contains(buttonElement)).to.be.true;
    });

    test('calls onClick handler only once', () => {
        const mockOnClick = vi.fn();
        render(<Button title="Test Button" onClick={mockOnClick} />);

        const button = screen.getByText('Test Button');
        fireEvent.click(button);
        fireEvent.click(button); // second click

        expect(mockOnClick).toHaveBeenCalledTimes(1);
    });

    test('does not call onClick when disabled is true', () => {
        const mockOnClick = vi.fn();
        render(<Button title="Test Button" onClick={mockOnClick} disabled={true} />);

        const button = screen.getByText('Test Button');
        fireEvent.click(button);

        expect(mockOnClick).not.toHaveBeenCalled();
    });

    test('applies custom class and style', () => {
        const style = { backgroundColor: 'blue' };
        render(<Button title="Test Button" className="custom-class" style={style} />);

        const button = screen.getByText('Test Button');
        expect(button.classList.contains('custom-class')).to.be.true;
        expect(button.style.backgroundColor).toBe('blue');
    });

});
