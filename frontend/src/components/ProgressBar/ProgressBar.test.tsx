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

    it('hides percentage when showPercentage is false', () => {
        const { container } = render(<ProgressBar value={75} showPercentage={false} />);
        const percentageElement = container.querySelector('.aml__progress-bar-content-percentage');
        expect(percentageElement).toBeFalsy();
    });

    it('calculates percentage correctly with custom max value when showPercentage is true', () => {
        const { container, getByText } = render(<ProgressBar value={150} max={200} showPercentage={true} />);
        const progressFill = container.querySelector('.aml__progress-bar-fill');

        expect(progressFill?.getAttribute('style')).toBe('width: 75%;');
        expect(getByText('75%')).toBeTruthy();
    });

    it('displays both label and percentage when both are provided', () => {
        const { getByText } = render(<ProgressBar value={50} label="Loading..." showPercentage={true} />);

        expect(getByText('Loading...')).toBeTruthy();
        expect(getByText('50%')).toBeTruthy();
    });
});
