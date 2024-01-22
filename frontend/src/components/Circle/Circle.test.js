import React from 'react';
import { render, waitFor } from '@testing-library/react';
import Circle from './Circle';

const Timer = jest.requireActual('util/timer');

let timerSpy;

global.performance = {
    now: () => Date.now(),
};

describe('Circle', () => {

    beforeEach(() => {
        timerSpy = jest.spyOn(Timer, 'default');

        // mock requestAnimationFrame
        let time = 0
        jest.spyOn(window, 'requestAnimationFrame').mockImplementation(
            // @ts-expect-error
            (cb) => {
                // we can then use fake timers to preserve the async nature of this call

                setTimeout(() => {
                    time = time + 16 // 16 ms
                    cb(time)
                }, 0)
            })
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    it('renders correctly with default props', () => {
        const { container } = render(<Circle />);
        expect(container.querySelector('.aha__circle')).toBeInTheDocument();
        expect(container.querySelectorAll('circle').length).toBe(2);
    });

    it('calls onTick and onFinish callbacks when running is true', async () => {
        const onTick = jest.fn();
        const onFinish = jest.fn();

        render(
            <Circle
                onTick={onTick}
                onFinish={onFinish}
                startTime={0}
                duration={1}
                running={true}

            />
        );

        await waitFor(() => expect(onTick).toHaveBeenCalled());
        await waitFor(() => expect(onFinish).toHaveBeenCalled());
    });

    it('does not start timer when running is false', () => {
        const onTick = jest.fn();
        const onFinish = jest.fn();
        render(<Circle running={false} onTick={onTick} onFinish={onFinish} duration={100} />);

        expect(timerSpy).not.toHaveBeenCalled();
        expect(onTick).not.toHaveBeenCalled();
        expect(onFinish).not.toHaveBeenCalled();
    });

    it('calculates style for circle animation correctly', () => {
        const time = 50;
        const duration = 100;
        const { container } = render(<Circle time={time} duration={duration} running={true} animateCircle={true} />);

        const percentageCircle = container.querySelector('.circle-percentage');

        expect(percentageCircle).toHaveStyle('stroke-dashoffset: 0.5340707511102648;');
    });

});
