import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import AutoPlay from '@/components/Playback/Autoplay';

// Mock the Circle and ListenCircle components
vi.mock('../Circle/Circle', () => ({
    default: vi.fn(({ onFinish }) => (
        <div data-testid="mock-circle" onClick={onFinish}>Mock Circle</div>
    )),
}));

vi.mock('../CountDown/CountDown', () => ({
    default: vi.fn(() => <div data-testid="mock-countdown">Mock Countdown</div>),
}));

vi.mock('../Histogram/Histogram', () => ({
    default: vi.fn(() => <div data-testid="mock-histogram">Mock Histogram</div>),
}));

describe('AutoPlay Component', () => {
    const mockPlaySection = vi.fn();
    const mockFinishedPlaying = vi.fn();

    const defaultProps = {
        sections: [{link: 'audio/to/play.mp3'}],
        showAnimation: true,
        playSection: mockPlaySection,
        startedPlaying: false,
        finishedPlaying: mockFinishedPlaying,
        responseTime: 5000,
    };

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('renders correctly with animation', () => {
        const { container } = render(<AutoPlay {...defaultProps} />);
        expect(container.querySelector('.circle')).toBeTruthy();
        expect(screen.getByTestId('mock-circle')).toBeTruthy();
        expect(screen.queryByTestId('mock-countdown')).toBeTruthy();
        expect(screen.queryByTestId('mock-histogram')).toBeTruthy();
    });

    it('renders correctly without animation', () => {
        const { container } = render(<AutoPlay {...defaultProps} showAnimation={false} />);
        expect(container.querySelector('.circle')).toBeTruthy();
        expect(screen.getByTestId('mock-circle')).toBeTruthy();
        expect(screen.queryByTestId('mock-countdown')).toBeFalsy();
        expect(screen.queryByTestId('mock-histogram')).toBeFalsy();
        expect(container.querySelector('.stationary')).toBeTruthy();
        expect(container.querySelector('.fa-headphones')).toBeTruthy();
    });

    it('calls playSection on mount', () => {
        render(<AutoPlay {...defaultProps} />);
        expect(mockPlaySection).toHaveBeenCalledWith(0);
    });

    it('calls finishedPlaying when Circle onFinish is triggered', () => {
        render(<AutoPlay {...defaultProps} />);
        const mockCircle = screen.getByTestId('mock-circle');
        mockCircle.click(); // Simulate onFinish
        expect(mockFinishedPlaying).toHaveBeenCalled();
    });

    it('renders instruction when provided', () => {
        const instruction = 'Test instruction';
        render(<AutoPlay {...defaultProps} instruction={instruction} />);
        expect(screen.getByText(instruction)).toBeTruthy();
    });

    it('applies custom className', () => {
        const customClass = 'custom-class';
        const { container } = render(<AutoPlay {...defaultProps} className={customClass} />);
        const listenDiv = container.querySelector('.aha__autoplay');
        expect(listenDiv.classList.contains(customClass)).toBe(true);
    });

    it('applies default classes to surrounding div', () => {
        const { container } = render(<AutoPlay {...defaultProps} />);
        const listenDiv = container.querySelector('.aha__autoplay');
        expect(listenDiv.classList.contains('d-flex')).toBe(true);
        expect(listenDiv.classList.contains('flex-column')).toBe(true);
        expect(listenDiv.classList.contains('justify-content-center')).toBe(true);
        expect(listenDiv.classList.contains('align-items-center')).toBe(true);
    });
});
