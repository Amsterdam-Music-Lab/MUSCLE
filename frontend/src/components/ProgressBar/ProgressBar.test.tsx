import { render } from '@testing-library/react';
import ProgressBar from './ProgressBar';
import { describe, it, expect } from 'vitest';

describe('ProgressBar', () => {
    it('renders correctly with default props', () => {
        const { container } = render(<ProgressBar value={50} />);

        const progressBar = container.querySelector('.aml__progress-bar');
        const progressFill = container.querySelector('.aml__progress-bar-fill');
        const content = container.querySelector('.aml__progress-bar-content');

        expect(progressBar).toBeTruthy();
        expect(progressFill).toBeTruthy();
        expect(content).toBeTruthy();
        expect(progressFill?.getAttribute('style')).toBe('width: 50%;');
    });

    it('clamps values to be between 0 and max', () => {
        const { container: containerNegative } = render(<ProgressBar value={-20} />);
        const { container: containerOverMax } = render(<ProgressBar value={150} />);

        const fillNegative = containerNegative.querySelector('.aml__progress-bar-fill');
        const fillOverMax = containerOverMax.querySelector('.aml__progress-bar-fill');

        expect(fillNegative?.getAttribute('style')).toBe('width: 0%;');
        expect(fillOverMax?.getAttribute('style')).toBe('width: 100%;');
    });

    it('displays label when provided', () => {
        const { getByText } = render(<ProgressBar value={50} label="Loading..." />);
        expect(getByText('Loading...')).toBeTruthy();
    });

    it('does not show percentage by default', () => {
        const { queryByText } = render(<ProgressBar value={75} />);

        const percentageElement = queryByText('75%');
        expect(percentageElement).toBeNull();
    });

    it('calculates percentage correctly with custom max value', () => {
        const { container } = render(<ProgressBar value={150} max={200} />);
        const progressFill = container.querySelector('.aml__progress-bar-fill');

        expect(progressFill?.getAttribute('style')).toBe('width: 75%;');
    });
});
