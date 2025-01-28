import { render, screen, fireEvent } from '@testing-library/react';
import { describe, test, expect, beforeEach, vi } from 'vitest';
import MultiPlayer from './MultiPlayer';

describe('MultiPlayer Component', () => {
    const mockPlaySection = vi.fn();
    const mockSections = [
        { id: '1', url: '123451' },
        { id: '2', url: '123452' },
        { id: '3', url: '123453' },
    ];

    const defaultProps = {
        playSection: mockPlaySection,
        sections: mockSections,
        playerIndex: '0',
        labels: { '0': 'Label 1', '1': 'Label 2', '2': 'Label 3' },
    };

    beforeEach(() => {
        vi.clearAllMocks();
    });

    test('renders correct number of PlayerSmall components', () => {
        render(<MultiPlayer {...defaultProps} />);
        const players = screen.getAllByTestId('player-small');
        expect(players.length).toBe(mockSections.length);
    });

    test('applies correct class names', () => {
        const { container } = render(<MultiPlayer {...defaultProps} />);

        if (!container.firstChild) {
            throw new Error('No container.firstChild');
        }

        const classList = container.firstChild.classList;

        expect(classList.contains('aha__multiplayer')).toBe(true);
        expect(classList.contains('d-flex')).toBe(true);
        expect(classList.contains('justify-content-around')).toBe(true);
        expect(classList.contains('player-count-3')).toBe(true);
    });

    test('calls playSection with correct index when PlayerSmall is clicked', () => {
        render(<MultiPlayer {...defaultProps} />);
        const players = screen.getAllByTestId('player-small');
        fireEvent.click(players[1]);
        expect(mockPlaySection).toHaveBeenCalledWith(1);
    });

    test('applies correct label to PlayerSmall components', () => {
        render(<MultiPlayer {...defaultProps} />);
        expect(screen.getByText('Label 1')).toBeTruthy();
        expect(screen.getByText('Label 2')).toBeTruthy();
        expect(screen.getByText('Label 3')).toBeTruthy();
    });

    test('renders extraContent when provided', () => {
        const extraContent = (index: string) => <span data-testid={`extra-${index}`}>Extra {index}</span>;
        render(<MultiPlayer {...defaultProps} extraContent={extraContent} />);
        expect(screen.getByTestId('extra-0')).toBeTruthy();
        expect(screen.getByTestId('extra-1')).toBeTruthy();
        expect(screen.getByTestId('extra-2')).toBeTruthy();
    });

    test('applies custom styles when provided', () => {
        const customStyle = {'custom-root-class': true };
        const { container } = render(<MultiPlayer {...defaultProps} style={customStyle} />);
        expect(container.firstChild.classList.contains('custom-root-class')).toBe(true);
    });
});
