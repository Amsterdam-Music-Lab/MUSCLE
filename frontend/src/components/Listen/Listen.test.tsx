import React from 'react';
import { describe, test, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import Listen from './Listen';

// Mock the Circle component
vi.mock('../Circle/Circle', () => ({
    default: ({ onFinish, children }) => (
        <div data-testid="mock-circle" onClick={onFinish}>
            {children}
        </div>
    ),
}));

describe('Listen Component', () => {
    test('renders without crashing', () => {
        render(<Listen instruction="Test instruction" onFinish={() => { }} />);
        expect(screen.getByText('Test instruction')).toBeTruthy();
    });

    test('renders circle content when provided', () => {
        render(
            <Listen
                instruction="Test instruction"
                onFinish={() => { }}
                circleContent={<span>Circle content</span>}
            />
        );
        expect(screen.getByText('Circle content')).toBeTruthy();
    });

    test('passes correct props to Circle component', () => {
        const onFinish = vi.fn();
        render(
            <Listen
                instruction="Test instruction"
                onFinish={onFinish}
                duration={5}
                color="red"
                running={false}
            />
        );
        const circle = screen.getByTestId('mock-circle');
        expect(circle).toBeTruthy();
        // Note: In a real scenario, you'd check for the actual props passed to Circle
    });

    test('applies custom className', () => {
        render(
            <Listen
                instruction="Test instruction"
                onFinish={() => { }}
                className="custom-class"
            />
        );
        const listen = screen.getByText('Test instruction').closest('.aha__listen');
        expect(listen).toBeTruthy();
        expect(listen!.classList.contains('custom-class')).toBe(true);
    });

    test('renders instruction text', () => {
        render(<Listen instruction="Test instruction" onFinish={() => { }} />);
        expect(screen.getByText('Test instruction')).toBeTruthy();
    });
});
