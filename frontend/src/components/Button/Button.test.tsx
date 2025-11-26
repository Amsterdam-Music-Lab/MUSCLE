import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import Button from './Button';
import { describe, expect, it, vi } from 'vitest';

describe('Button component', () => {

    it('renders correctly', () => {
        const mockOnClick = vi.fn();
        const { getByText } = render(<Button label="Test Button" onClick={mockOnClick} color="#fabacc" />);
        const buttonElement = getByText('Test Button');

        expect(document.body.contains(buttonElement)).toBe(true);
    });

    it('calls onClick when button is clicked', () => {
        const onNextMock = vi.fn();
        render(<Button label="Click me" onClick={onNextMock} />);
        fireEvent.click(screen.getByText('Click me'));
        expect(onNextMock).toHaveBeenCalledTimes(1);
    });

    it('calls onClick handler only once', () => {
        const mockOnClick = vi.fn();
        const { getByText } = render(<Button label="Test Button" onClick={mockOnClick} color="#fabacc"/>);

        const button = getByText('Test Button');
        fireEvent.click(button);
        fireEvent.click(button); // second click

        expect(mockOnClick).toHaveBeenCalledTimes(1);
    });

    it('does not call onClick when disabled is true', () => {
        const mockOnClick = vi.fn();
        const { getByText } = render(<Button label="Test Button" onClick={mockOnClick} disabled={true} color="#fabacc"/>);

        const button = getByText('Test Button');
        fireEvent.click(button);

        expect(mockOnClick).not.toHaveBeenCalled();
    });

    it('applies custom class and style', () => {
        const mockOnClick = vi.fn();
        const style = { backgroundColor: 'blue' };
        const { getByText } = render(<Button label="Test Button" className="custom-class" style={style} onClick={mockOnClick} color="#fabacc" />);

        const button = getByText('Test Button');
        
        expect(button.classList.contains('custom-class')).toBe(true);
        expect(button.style.backgroundColor).toBe('blue');
    });

    test('renders anchor tag when button label & button link are provided', () => {
        render(<Button label="Click me" link="https://example.com" />);
        const anchor = screen.getByText('Click me');
        expect(anchor).toBeTruthy();
        expect(anchor?.textContent).toBe('Click me');
        expect(anchor.tagName).toBe('A');
    });

    test('renders button when label & onClick is provided', () => {
        render(<Button label="Click me" onClick={vi.fn()} />);
        const button = screen.queryByRole('button');
        expect(button).toBeTruthy();
        expect(button?.textContent).toBe('Click me');
        expect(button?.tagName).toBe('BUTTON');
    });

        test('renders anchor tag when link is provided', () => {
        render(<Button label="Click me" link="https://example.com"/>);
        const anchor = screen.getByText('Click me');
        expect(anchor.tagName).toBe('A');
        expect(anchor.getAttribute('href')).toBe('https://example.com');
        expect(anchor.getAttribute('target')).toBe('_blank');
        expect(anchor.getAttribute('rel')).toBe('noopener noreferrer');
    });

    test('renders button without link when only button label is provided', () => {
        render(<Button body="Test body" label="Click me" onClick={vi.fn()} />);
        const button = screen.getByText('Click me');
        expect(button.tagName).toBe('BUTTON');
    });

});
