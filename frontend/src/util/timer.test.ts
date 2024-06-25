import { beforeEach, afterEach, describe, it, expect, vi } from 'vitest';
import Timer from './timer';

describe('Timer', () => {
    let originalRequestAnimationFrame: any;
    let now = 0;

    beforeEach(() => {
        // Use fake timers
        vi.useFakeTimers();
        now = 0;
        vi.spyOn(performance, 'now').mockImplementation(() => now);

        // Mock requestAnimationFrame
        originalRequestAnimationFrame = window.requestAnimationFrame;
        window.requestAnimationFrame = (cb) => {
            setTimeout(() => {
                now += 1000 / 60; // Simulate 60fps
                cb(performance.now());
            }, 1000 / 60);
        };
    });

    afterEach(() => {
        // Clear all timers and mocks
        vi.clearAllTimers();
        vi.restoreAllMocks();
        window.requestAnimationFrame = originalRequestAnimationFrame;
    });

    it('should call onTick at intervals', () => {
        const onTick = vi.fn();
        const duration = 2;
        const interval = 0.5;
        const stop = Timer({
            duration,
            onTick,
            interval,
        });
        // The number of ticks should be ceil(duration / interval) - 1
        // as there is no tick when it finishes
        const expectedTicks = Math.ceil(duration / interval) - 1;

        // Advance the timer by 3 seconds
        vi.advanceTimersByTime(3000);

        // Check that onTick was called the correct number of times
        expect(onTick).toHaveBeenCalledTimes(expectedTicks);

        stop();
    });

    it('should call onFinish when the duration is reached', () => {
        const onFinish = vi.fn();
        const duration = 1;
        const stop = Timer({
            duration,
            onFinish,
        });

        // Advance the timer by 2 seconds
        vi.advanceTimersByTime(2000);

        // Check that onFinish was called once
        expect(onFinish).toHaveBeenCalledTimes(1);

        stop();
    });

    it('should stop the timer when stop function is called', () => {
        const onTick = vi.fn();
        const duration = 2;
        const interval = 0.5;
        const stop = Timer({
            duration,
            onTick,
            interval,
        });

        // Advance the timer by 1 second
        vi.advanceTimersByTime(1000);

        // Stop the timer
        stop();

        // Advance the timer by another 1 second
        vi.advanceTimersByTime(1000);

        // Check that onTick was called only for the first second
        expect(onTick).toHaveBeenCalledTimes(2); // Should be called twice before stopping

        stop();
    });

    it('should correctly handle the initial time parameter', () => {
        const onTick = vi.fn();
        const onFinish = vi.fn();
        const duration = 3;
        const interval = 0.5;
        const time = 1;
        const stop = Timer({
            time,
            duration,
            onFinish,
            onTick,
            interval,
        });

        // Advance the timer by 500ms
        vi.advanceTimersByTime(500);

        expect(onFinish).not.toHaveBeenCalled(); // Should not have finished yet
        expect(onTick).toHaveBeenCalledTimes(1); // Should have ticked once

        // Advance the timer by another 500ms
        vi.advanceTimersByTime(500);

        expect(onFinish).not.toHaveBeenCalled(); // Should not have finished yet
        expect(onTick).toHaveBeenCalledTimes(2); // Should have ticked twice

        // Advance the timer by another 500ms
        vi.advanceTimersByTime(500);

        expect(onFinish).not.toHaveBeenCalled(); // Should not have finished yet
        expect(onTick).toHaveBeenCalledTimes(3); // Should have ticked twice

        // Advance the timer by another 500ms
        vi.advanceTimersByTime(500);

        // Check that onFinish was called once
        expect(onFinish).toHaveBeenCalledTimes(1);
        expect(onTick).toHaveBeenCalledTimes(3); // No extra tick after finishing
        
        stop();
    });
});