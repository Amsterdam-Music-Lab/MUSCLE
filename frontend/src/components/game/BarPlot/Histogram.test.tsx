// import { describe, it, expect, vi, beforeEach, afterEach, Mock, } from 'vitest';
// import { render, act } from '@testing-library/react';
// import Histogram from './Histogram';

// // Mock requestAnimationFrame and cancelAnimationFrame
// vi.stubGlobal('requestAnimationFrame', (callback: FrameRequestCallback): number => {
//     return setTimeout(callback, 16); // Approximate 60 FPS
// });

// vi.stubGlobal('cancelAnimationFrame', (handle: number): void => {
//     clearTimeout(handle);
// });

// // Mock setInterval and clearInterval
// vi.useFakeTimers();

// vi.mock('../../util/stores', () => ({
//     __esModule: true,
//     default: (fn: any) => {
//         const state = {
//             currentAction: { playback: { play_method: 'BUFFER' } },
//         };

//         return fn(state);
//     },
//     useBoundStore: vi.fn()
// }));

// describe('Histogram', () => {
//     let mockAnalyser: {
//         getByteFrequencyData: Mock
//     };

//     beforeEach(() => {
//         // Mock the Web Audio API
//         mockAnalyser = {
//             getByteFrequencyData: vi.fn(),
//         };

//         (global as any).window.audioContext = {};
//         (global as any).window.analyzer = mockAnalyser;
//     });

//     afterEach(() => {
//         vi.clearAllTimers();
//         vi.restoreAllMocks();
//     });

//     it('renders the correct number of bars', () => {
//         const { container } = render(<Histogram bars={5} />);
//         const bars = container.querySelectorAll('.aha__histogram > div');
//         expect(bars.length).to.equal(5);
//     });

//     it('applies the correct spacing between bars', () => {
//         const { container } = render(<Histogram bars={3} spacing={10} />);
//         const bars = container.querySelectorAll('.aha__histogram > div');
//         expect(getComputedStyle(bars[0]).marginRight).to.equal('10px');
//         expect(getComputedStyle(bars[1]).marginRight).to.equal('10px');
//         expect(getComputedStyle(bars[2]).marginRight).to.equal('0px');
//     });

//     it('applies the correct margin and background color', () => {
//         const { container } = render(
//             <Histogram marginLeft={20} marginTop={10} backgroundColor="red" />
//         );
//         const histogram = container.querySelector('.aha__histogram');

//         if (!histogram) {
//             throw new Error('Histogram not found');
//         }

//         expect(getComputedStyle(histogram).marginLeft).to.equal('20px');
//         expect(getComputedStyle(histogram).marginTop).to.equal('10px');
//         expect(getComputedStyle(histogram).backgroundColor).to.equal('red');
//     });

//     it('applies the correct border radius', () => {
//         const { container } = render(<Histogram borderRadius="5px" />);
//         const histogram = container.querySelector('.aha__histogram');

//         if (!histogram) {
//             throw new Error('Histogram not found');
//         }

//         expect(getComputedStyle(histogram).borderRadius).to.equal('5px');
//     });

//     it('has active class when running', () => {
//         const { container } = render(<Histogram running={true} />);
//         const histogram = container.querySelector('.aha__histogram');

//         if (!histogram) {
//             throw new Error('Histogram not found');
//         }

//         expect(histogram.classList.contains('active')).toBe(true);
//     });

//     it('does not have active class when not running', () => {
//         const { container } = render(<Histogram running={false} />);
//         const histogram = container.querySelector('.aha__histogram');

//         if (!histogram) {
//             throw new Error('Histogram not found');
//         }

//         expect(histogram.classList.contains('active')).toBe(false);
//     });

//     it('updates bar heights based on frequency data when running', async () => {
//         const bars = 5;
//         mockAnalyser.getByteFrequencyData.mockImplementation((array) => {
//             for (let i = 0; i < array.length; i++) {
//                 array[i] = Math.floor(Math.random() * 256);
//             }
//         });

//         const { container, rerender } = render(<Histogram running={true} bars={bars} />);

//         const getHeights = () => Array.from(container.querySelectorAll('.aha__histogram > div')).map(
//             (bar) => bar.style.height
//         );

//         const initialHeights = getHeights();

//         // Advance timers and trigger animation frame
//         await act(async () => {
//             vi.advanceTimersByTime(100);
//         });

//         rerender(<Histogram running={true} bars={bars} />);

//         const updatedHeights = getHeights();

//         expect(initialHeights).not.to.deep.equal(updatedHeights);
//         expect(mockAnalyser.getByteFrequencyData).toHaveBeenCalled();
//     });

//     it('does not update bar heights when not running', () => {
//         const bars = 5;
//         mockAnalyser.getByteFrequencyData.mockImplementation(() => {
//             // This should not be called when running is false
//         });

//         const { container } = render(<Histogram running={false} bars={bars} />);

//         const getHeights = () =>
//             Array.from(container.querySelectorAll('.aha__histogram > div')).map(
//                 (bar) => bar.style.height
//             );

//         const initialHeights = getHeights();

//         // Advance timers to simulate time passing
//         act(() => {
//             vi.advanceTimersByTime(1000); // Advance time by 1 second
//         });

//         const updatedHeights = getHeights();

//         expect(initialHeights).to.deep.equal(updatedHeights);
//         expect(mockAnalyser.getByteFrequencyData).not.toHaveBeenCalled();
//     });

//     it('updates bar heights based on random data when random is true and running is true', async () => {
//         const bars = 5;

//         const { container, rerender } = render(
//             <Histogram running={true} bars={bars} random={true} interval={200} />
//         );

//         const getHeights = () =>
//             Array.from(container.querySelectorAll('.aha__histogram > div')).map(
//                 (bar) => bar.style.height
//             );

//         const initialHeights = getHeights();

//         // Advance timers by at least one interval
//         await act(async () => {
//             vi.advanceTimersByTime(200);
//         });

//         rerender(<Histogram running={true} bars={bars} random={true} />);

//         const updatedHeights = getHeights();

//         expect(initialHeights).not.to.deep.equal(updatedHeights);
//     });

//     it('does not call getByteFrequencyData when random is true', async () => {
//         const bars = 5;

//         const { rerender } = render(
//             <Histogram running={true} bars={bars} random={true} />
//         );

//         // Advance timers and trigger animation frame
//         await act(async () => {
//             vi.advanceTimersByTime(100);
//         });

//         rerender(<Histogram running={true} bars={bars} random={true} />);

//         expect(mockAnalyser.getByteFrequencyData).not.toHaveBeenCalled();
//     });

//     it('updates bar heights based on random data at the specified interval', async () => {
//         const bars = 5;
//         const interval = 200;

//         const { container } = render(
//             <Histogram running={true} bars={bars} random={true} interval={interval} />
//         );

//         const getHeights = () =>
//             Array.from(container.querySelectorAll('.aha__histogram > div')).map(
//                 (bar) => bar.style.height
//             );

//         const initialHeights = getHeights();

//         // Advance timers by the interval to trigger the update
//         await act(async () => {
//             vi.advanceTimersByTime(interval);
//         });

//         const updatedHeights = getHeights();

//         expect(initialHeights).not.to.deep.equal(updatedHeights);
//     });

//     it('updates bar heights based on frequency data using requestAnimationFrame', async () => {
//         const bars = 5;

//         mockAnalyser.getByteFrequencyData.mockImplementation((array) => {
//             for (let i = 0; i < array.length; i++) {
//                 array[i] = Math.floor(Math.random() * 256);
//             }
//         });

//         const { container } = render(<Histogram running={true} bars={bars} />);

//         const getHeights = () =>
//             Array.from(container.querySelectorAll('.aha__histogram > div')).map(
//                 (bar) => bar.style.height
//             );

//         const initialHeights = getHeights();

//         // Advance timers to simulate requestAnimationFrame calls
//         await act(async () => {
//             vi.advanceTimersByTime(16); // Approximate time for one frame at 60 FPS
//         });

//         const updatedHeights = getHeights();

//         expect(initialHeights).not.to.deep.equal(updatedHeights);
//         expect(mockAnalyser.getByteFrequencyData).toHaveBeenCalled();
//     });
// });
