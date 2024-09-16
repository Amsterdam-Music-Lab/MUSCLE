import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import AutoPlay from '@/components/Playback/Autoplay';

// Mock the Circle and ListenCircle components
vi.mock('../Circle/Circle', () => ({
    default: vi.fn(({ onFinish }) => (
        <div data-testid="mock-circle" onClick={onFinish}>Mock Circle</div>
    )),
}));

vi.mock('../ListenCircle/ListenCircle', () => ({
    default: vi.fn(() => <div data-testid="mock-listen-circle">Mock Listen Circle</div>),
}));

describe('AutoPlay Component', () => {
    const mockPlaySection = vi.fn();
    const mockFinishedPlaying = vi.fn();

    const defaultProps = {
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
        expect(screen.getByTestId('mock-listen-circle')).toBeTruthy();
    });

    it('renders correctly without animation', () => {
        const { container } = render(<AutoPlay {...defaultProps} showAnimation={false} />);
        expect(container.querySelector('.circle')).toBeTruthy();
        expect(screen.getByTestId('mock-circle')).toBeTruthy();
        expect(screen.queryByTestId('mock-listen-circle')).toBeFalsy();
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
        const listenDiv = container.querySelector('.aha__listen');
        expect(listenDiv.classList.contains(customClass)).toBe(true);
    });

    it('applies default classes to listen div', () => {
        const { container } = render(<AutoPlay {...defaultProps} />);
        const listenDiv = container.querySelector('.aha__listen');
        expect(listenDiv.classList.contains('d-flex')).toBe(true);
        expect(listenDiv.classList.contains('flex-column')).toBe(true);
        expect(listenDiv.classList.contains('justify-content-center')).toBe(true);
        expect(listenDiv.classList.contains('align-items-center')).toBe(true);
    });
});
