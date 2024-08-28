import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import PlayerSmall from './PlayerSmall';

// Mock the PlayButton component
vi.mock('./PlayButton', () => ({
    default: vi.fn(() => <div data-testid="mock-play-button">Mock Play Button</div>),
}));

describe('PlayerSmall Component', () => {
    const mockOnClick = vi.fn();

    const defaultProps = {
        onClick: mockOnClick,
        playing: false,
    };

    it('renders correctly without label', () => {
        const { container } = render(<PlayerSmall {...defaultProps} />);
        expect(container.querySelector('.aha__player-small')).toBeTruthy();
        expect(screen.getByTestId('mock-play-button')).toBeTruthy();
        expect(container.querySelector('.label')).toBeFalsy();
    });

    it('renders correctly with label', () => {
        const label = 'Test Label';
        const { container } = render(<PlayerSmall {...defaultProps} label={label} />);
        expect(container.querySelector('.aha__player-small')).toBeTruthy();
        expect(screen.getByTestId('mock-play-button')).toBeTruthy();
        expect(screen.getByText(label)).toBeTruthy();
        expect(container.querySelector('.banner')).toBeTruthy();
    });

    it('applies correct classes', () => {
        const { container } = render(<PlayerSmall {...defaultProps} />);
        const playerSmall = container.querySelector('.aha__player-small');
        expect(playerSmall.classList.contains('anim')).toBe(true);
        expect(playerSmall.classList.contains('anim-fade-in')).toBe(true);
    });

    it('applies hasLabel class when label is provided', () => {
        const { container } = render(<PlayerSmall {...defaultProps} label="Test Label" />);
        const playerSmall = container.querySelector('.aha__player-small');
        expect(playerSmall.classList.contains('hasLabel')).toBe(true);
    });

    it('applies disabled class when disabled prop is true', () => {
        const { container } = render(<PlayerSmall {...defaultProps} disabled={true} />);
        const playerSmall = container.querySelector('.aha__player-small');
        expect(playerSmall.classList.contains('disabled')).toBe(true);
    });

    it('calls onClick when clicked', () => {
        render(<PlayerSmall {...defaultProps} />);
        const playerSmall = screen.getByTestId('player-small');
        fireEvent.click(playerSmall);
        expect(mockOnClick).toHaveBeenCalled();
    });

    it('passes correct props to PlayButton', () => {
        const { rerender } = render(<PlayerSmall {...defaultProps} />);
        expect(screen.getByTestId('mock-play-button')).toBeTruthy();

        rerender(<PlayerSmall {...defaultProps} playing={true} disabled={true} />);
        expect(screen.getByTestId('mock-play-button')).toBeTruthy();
    });

    it('has correct accessibility attributes', () => {
        const { container } = render(<PlayerSmall {...defaultProps} />);
        const playerSmall = container.querySelector('.aha__player-small');
        expect(playerSmall.getAttribute('role')).toBe('button');
    });
});
