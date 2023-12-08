import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Button from './Button';

describe('Button component', () => {

    it('renders correctly', () => {
        render(<Button title="Test Button" />);
        expect(screen.getByText('Test Button')).toBeInTheDocument();
    });

    test('calls onClick handler only once', () => {
        const mockOnClick = jest.fn();
        render(<Button title="Test Button" onClick={mockOnClick} />);

        const button = screen.getByText('Test Button');
        fireEvent.click(button);
        fireEvent.click(button); // second click

        expect(mockOnClick).toHaveBeenCalledTimes(1);
    });

    test('does not call onClick when active is false', () => {
        const mockOnClick = jest.fn();
        render(<Button title="Test Button" onClick={mockOnClick} active={false} />);

        const button = screen.getByText('Test Button');
        fireEvent.click(button);

        expect(mockOnClick).not.toHaveBeenCalled();
    });

    test('applies custom class and style', () => {
        const style = { backgroundColor: 'blue' };
        render(<Button title="Test Button" className="custom-class" style={style} />);

        const button = screen.getByText('Test Button');
        expect(button).toHaveClass('custom-class');
        expect(button).toHaveStyle('background-color: blue');
    });

});
