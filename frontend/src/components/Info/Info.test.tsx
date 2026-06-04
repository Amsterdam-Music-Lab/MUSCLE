import { describe, test, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
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

    test('does not render button when button props are not provided', () => {
        render(<Info body="Test body" />);
        expect(screen.queryByRole('button')).toBeNull();
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
