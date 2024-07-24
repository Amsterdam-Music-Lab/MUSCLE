import { describe, test, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Info from './Info';

describe('Info Component', () => {
    test('renders without crashing', () => {
        render(<Info body="Test body" />);
        expect(screen.getByText('Test body')).toBeTruthy();
    });

    test('renders heading when provided', () => {
        render(<Info heading="Test Heading" body="Test body" />);
        expect(screen.getByText('Test Heading')).toBeTruthy();
    });

    test('does not render heading when not provided', () => {
        render(<Info body="Test body" />);
        expect(screen.queryByRole('heading')).toBeNull();
    });

    test('renders button link when button_label & button_link is provided', () => {
        render(<Info body="Test body" button_label="Click me" button_link="https://example.com" />);
        const anchor = screen.getByText('Click me');
        expect(anchor).toBeTruthy();
        expect(anchor?.textContent).toBe('Click me');
        expect(anchor.tagName).toBe('A');
    });

    test('renders button when button_label & onNext is provided', () => {
        render(<Info body="Test body" button_label="Click me" onNext={vi.fn()} />);
        const button = screen.queryByRole('button');
        expect(button).toBeTruthy();
        expect(button?.textContent).toBe('Click me');
        expect(button?.tagName).toBe('BUTTON');
    });

    test('does not render button without link and onNext when only button_label is provided', () => {
        render(<Info body="Test body" button_label="Click me" />);
        expect(screen.queryByRole('button')).toBeNull();
    });

    test('does not render button when button_label is not provided', () => {
        render(<Info body="Test body" />);
        expect(screen.queryByRole('button')).toBeNull();
    });

    test('renders anchor tag when button_link is provided', () => {
        render(<Info body="Test body" button_label="Click me" button_link="https://example.com" />);
        const anchor = screen.getByText('Click me');
        expect(anchor.tagName).toBe('A');
        expect(anchor.getAttribute('href')).toBe('https://example.com');
        expect(anchor.getAttribute('target')).toBe('_blank');
        expect(anchor.getAttribute('rel')).toBe('noopener noreferrer');
    });

    test('renders button without link when only button_label is provided', () => {
        const onNextMock = vi.fn();
        render(<Info body="Test body" button_label="Click me" onNext={onNextMock} />);
        const button = screen.getByText('Click me');
        expect(button.tagName).toBe('BUTTON');
    });

    test('calls onNext when button is clicked', () => {
        const onNextMock = vi.fn();
        render(<Info body="Test body" button_label="Click me" onNext={onNextMock} />);
        fireEvent.click(screen.getByText('Click me'));
        expect(onNextMock).toHaveBeenCalledTimes(1);
    });

    test('renders body content as HTML', () => {
        render(<Info body="<p>Test <strong>body</strong></p>" />);
        const infoBody = screen.getByTestId('info-body');
        expect(infoBody.innerHTML).toBe('<p>Test <strong>body</strong></p>');
    });

    test('applies max-height style to info-body', () => {
        render(<Info body="Test body" />);
        const infoBody = screen.getByTestId('info-body');
        expect(infoBody?.style.maxHeight).toBeTruthy();
    });

    test('updates max-height on window resize', async () => {
        const { rerender } = render(<Info body="Test body" />);
        const initialHeight = screen.getByTestId('info-body').style.maxHeight;

        // Simulate window resize
        window.innerHeight = 1001;
        window.dispatchEvent(new Event('resize'));

        rerender(<Info body="Test body" />);

        const updatedHeight = screen.getByText('Test body').parentElement?.style.maxHeight;
        expect(updatedHeight).not.toBe(initialHeight);
    });
});
