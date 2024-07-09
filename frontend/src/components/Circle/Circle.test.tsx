import { render, waitFor } from '@testing-library/react';
import Circle from './Circle';
import { vi, describe, it, beforeEach, expect } from 'vitest';
import Timer from '@/util/timer';

vi.mock('@/util/timer', () => {
    return {
        Timer: vi.fn(),
        default: vi.fn(),
    };
});

global.performance = {
    now: () => Date.now(),
};

describe('Circle', () => {

    beforeEach(() => {
        // mock requestAnimationFrame
        let time = 0
        vi.spyOn(window, 'requestAnimationFrame').mockImplementation(
            // @ts-expect-error
            (cb) => {
                // we can then use fake timers to preserve the async nature of this call

                setTimeout(() => {
                    time = time + 16 // 16 ms
                    cb(time)
                }, 0)
            })

        Timer.mockReset();

        Timer.mockImplementation(({ onFinish, onTick }) => {
            onTick && onTick(0);
            onFinish && onFinish();
            return vi.fn();
        });
    });

    it('renders correctly with default props', () => {
        const { container } = render(<Circle />);

        expect(document.body.contains(container.querySelector('.aha__circle'))).toBe(true);
        expect(container.querySelectorAll('circle').length).toBe(2);
    });

    it('calls onTick and onFinish callbacks when running is true', async () => {


        const onTick = vi.fn();
        const onFinish = vi.fn();

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
        const onTick = vi.fn();
        const onFinish = vi.fn();
        render(<Circle running={false} onTick={onTick} onFinish={onFinish} duration={100} />);

        expect(Timer).not.toHaveBeenCalled();
        expect(onTick).not.toHaveBeenCalled();
        expect(onFinish).not.toHaveBeenCalled();
    });

    it('calculates style for circle animation correctly', () => {
        const time = 50;
        const duration = 100;
        const { container } = render(<Circle time={time} duration={duration} running={true} animateCircle={true} />);

        const percentageCircle = container.querySelector('.circle-percentage');

        expect(percentageCircle.style.strokeDashoffset).toEqual('0.5340707511102648');
    });

});
