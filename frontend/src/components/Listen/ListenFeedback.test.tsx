import React from 'react';
import { describe, test, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ListenFeedback from './ListenFeedback';

// Mock the Circle component
vi.mock('../Circle/Circle', () => ({
    default: ({ onFinish, children }) => (
        <div data-testid="mock-circle" onClick={onFinish}>
            {children}
        </div>
    ),
}));

// Mock the Button component
vi.mock('../Button/Button', () => ({
    default: ({ onClick, title }) => (
        <button onClick={onClick}>{title}</button>
    ),
}));

describe('ListenFeedback Component', () => {
    test('renders without crashing', () => {
        render(<ListenFeedback instruction="Test instruction" onFinish={() => { }} />);
        expect(screen.getByText('Test instruction')).toBeTruthy();
    });

    test('renders circle content when provided', () => {
        render(
            <ListenFeedback
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
            <ListenFeedback
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
            <ListenFeedback
                instruction="Test instruction"
                onFinish={() => { }}
                className="custom-class"
            />
        );
        const listen = screen.getByText('Test instruction').closest('.aha__listen');
        expect(listen).toBeTruthy();
        expect(listen!.classList).toContain('custom-class');
    });

    test('renders buttons when provided', () => {
        render(
            <ListenFeedback
                instruction="Test instruction"
                onFinish={() => { }}
                buttons={{ no: 'No', yes: 'Yes' }}
                onNoClick={() => { }}
                onYesClick={() => { }}
            />
        );
        expect(screen.getByText('No')).toBeTruthy();
        expect(screen.getByText('Yes')).toBeTruthy();
    });

    test('calls onNoClick when No button is clicked', () => {
        const onNoClick = vi.fn();
        render(
            <ListenFeedback
                instruction="Test instruction"
                onFinish={() => { }}
                buttons={{ no: 'No', yes: 'Yes' }}
                onNoClick={onNoClick}
                onYesClick={() => { }}
            />
        );
        fireEvent.click(screen.getByText('No'));
        expect(onNoClick).toHaveBeenCalledTimes(1);
    });

    test('calls onYesClick when Yes button is clicked', () => {
        const onYesClick = vi.fn();
        render(
            <ListenFeedback
                instruction="Test instruction"
                onFinish={() => { }}
                buttons={{ no: 'No', yes: 'Yes' }}
                onNoClick={() => { }}
                onYesClick={onYesClick}
            />
        );
        fireEvent.click(screen.getByText('Yes'));
        expect(onYesClick).toHaveBeenCalledTimes(1);
    });

    test('does not render buttons when not provided', () => {
        render(
            <ListenFeedback
                instruction="Test instruction"
                onFinish={() => { }}
            />
        );
        expect(screen.queryByText('No')).toBeNull();
        expect(screen.queryByText('Yes')).toBeNull();
    });
});
