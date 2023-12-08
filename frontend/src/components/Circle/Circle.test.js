import React from 'react';
import { render, waitFor } from '@testing-library/react';
import Circle from './Circle';
import Timer from 'util/timer';

global.requestAnimationFrame = (callback) => {
    setTimeout(callback, 0);
};
global.performance = {
    now: () => Date.now()
};

jest.mock('util/timer', () => ({
    __esModule: true,
    default: jest.fn(),
}));

describe('Circle', () => {

    afterEach(() => {
        jest.clearAllMocks();
    });

    it('renders correctly with default props', () => {
        const { container } = render(<Circle />);
        expect(container.querySelector('.aha__circle')).toBeInTheDocument();
        expect(container.querySelectorAll('circle').length).toBe(2);
    });

    it('calls onTick and onFinish callbacks', async () => {

        Timer.mockImplementation(({ onTick, onFinish, duration }) => {
            let time = 0;
            const interval = 10; // Simulate a timer interval
            const timerId = setInterval(() => {
                time += interval;
                if (onTick) {
                    onTick(time);
                }
                if (time >= duration) {
                    if (onFinish) {
                        onFinish();
                    }
                    clearInterval(timerId);
                }
            }, interval);
            return () => clearInterval(timerId);
        });

        const onTick = jest.fn();
        const onFinish = jest.fn();
        render(<Circle onTick={onTick} onFinish={onFinish} running={true} duration={100} />);

        await waitFor(() => expect(onTick).toHaveBeenCalled());
        await waitFor(() => expect(onFinish).toHaveBeenCalled());
    });

    it('starts timer when running is true', () => {
        const startTime = 0;
        const duration = 0;
        render(<Circle startTime={startTime} duration={duration} running={true} />);

        expect(Timer).toHaveBeenCalled();
    });

    it('calculates style for circle animation correctly', () => {
        const time = 50;
        const duration = 100;
        const { container } = render(<Circle time={time} duration={duration} running={true} animateCircle={true} />);

        const percentageCircle = container.querySelector('.circle-percentage');

        expect(percentageCircle).toHaveStyle('stroke-dashoffset: 0.5340707511102648;');
    });

    it('does not start timer when running is false', () => {
        const onTick = jest.fn();
        const onFinish = jest.fn();
        render(<Circle running={false} onTick={onTick} onFinish={onFinish} duration={100} />);

        expect(Timer).not.toHaveBeenCalled();
        expect(onTick).not.toHaveBeenCalled();
        expect(onFinish).not.toHaveBeenCalled();
    });

});
