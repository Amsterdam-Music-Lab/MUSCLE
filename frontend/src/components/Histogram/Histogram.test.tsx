import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render } from '@testing-library/react';
import Histogram from './Histogram';

describe('Histogram', () => {
    beforeEach(() => {
        vi.useFakeTimers();
    });

    it('renders the correct number of bars', () => {
        const { container } = render(<Histogram bars={5} />);
        const bars = container.querySelectorAll('.aha__histogram > div');
        expect(bars.length).to.equal(5);
    });

    it('applies the correct spacing between bars', () => {
        const { container } = render(<Histogram bars={3} spacing={10} />);
        const bars = container.querySelectorAll('.aha__histogram > div');
        expect(getComputedStyle(bars[0]).marginRight).to.equal('10px');
        expect(getComputedStyle(bars[1]).marginRight).to.equal('10px');
        expect(getComputedStyle(bars[2]).marginRight).to.equal('0px');
    });

    it('applies the correct margin and background color', () => {
        const { container } = render(
            <Histogram marginLeft={20} marginTop={10} backgroundColor="red" />
        );
        const histogram = container.querySelector('.aha__histogram');

        if (!histogram) {
            throw new Error('Histogram not found');
        }

        expect(getComputedStyle(histogram).marginLeft).to.equal('20px');
        expect(getComputedStyle(histogram).marginTop).to.equal('10px');
        expect(getComputedStyle(histogram).backgroundColor).to.equal('red');
    });

    it('applies the correct border radius', () => {
        const { container } = render(<Histogram borderRadius="5px" />);
        const histogram = container.querySelector('.aha__histogram');

        if (!histogram) {
            throw new Error('Histogram not found');
        }

        expect(getComputedStyle(histogram).borderRadius).to.equal('5px');
    });

    it('has active class when running', () => {
        const { container } = render(<Histogram running={true} />);
        const histogram = container.querySelector('.aha__histogram');

        if (!histogram) {
            throw new Error('Histogram not found');
        }

        expect(histogram.classList.contains('active')).toBe(true);
    });

    it('does not have active class when not running', () => {
        const { container } = render(<Histogram running={false} />);
        const histogram = container.querySelector('.aha__histogram');

        if (!histogram) {
            throw new Error('Histogram not found');
        }

        expect(histogram.classList.contains('active')).toBe(false);
    });

    it('updates bar heights when running', async () => {
        const { container, rerender } = render(<Histogram running={true} />);
        const getHeights = () => Array.from(container.querySelectorAll('.aha__histogram > div')).map(
            (bar) => bar.style.height
        );

        const initialHeights = getHeights();

        // Advance timer and force re-render
        vi.advanceTimersByTime(100);
        rerender(<Histogram running={true} />);

        const updatedHeights = getHeights();

        expect(initialHeights).not.to.deep.equal(updatedHeights);
    });

    it('does not update bar heights when not running', () => {
        const { container, rerender } = render(<Histogram running={false} />);
        const getHeights = () => Array.from(container.querySelectorAll('.aha__histogram > div')).map(
            (bar) => bar.style.height
        );

        const initialHeights = getHeights();

        // Advance timer and force re-render
        vi.advanceTimersByTime(100);
        rerender(<Histogram running={false} />);

        const updatedHeights = getHeights();

        expect(initialHeights).to.deep.equal(updatedHeights);
    });
});
