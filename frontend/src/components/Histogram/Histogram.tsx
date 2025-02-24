import React, { useEffect, useRef, useState } from 'react';
import classNames from 'classnames';
import useBoundStore from '@/util/stores';

interface HistogramProps {
    bars?: number;
    spacing?: number;
    running?: boolean;
    backgroundColor?: string;
    padding?: string;
    borderRadius?: string;
    random?: boolean;
    /**
     * If `random` is `true`, this prop sets the update interval in milliseconds.
     * Default is 100 ms.
     * Ignored when `random` is `false`.
     */
    interval?: number;
}

const Histogram: React.FC<HistogramProps> = ({
    bars = 8,
    spacing = 4,
    running = true,
    backgroundColor = undefined,
    borderRadius = '0.15rem',
    padding,
    random = false,
    interval = 200,
}) => {
    const [frequencyData, setFrequencyData] = useState<Uint8Array>(new Uint8Array(bars));

    const currentAction = useBoundStore((state) => state.currentAction);
    const isBuffer = currentAction?.playback?.play_method === 'BUFFER';

    const shouldRandomize = random || !isBuffer;

    const animationFrameRef = useRef<number>();
    const intervalRef = useRef<number>();

    useEffect(() => {
        if (!running) {
            if (animationFrameRef.current) {
                cancelAnimationFrame(animationFrameRef.current);
            }
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
            }
            const emptyHistogram = new Uint8Array(bars);
            setFrequencyData(emptyHistogram);
            return;
        }

        const updateFrequencyData = () => {
            let dataWithoutExtremes: Uint8Array;

            if (shouldRandomize) {
                // Generate random frequency data
                dataWithoutExtremes = new Uint8Array(bars);
                for (let i = 0; i < bars; i++) {
                    dataWithoutExtremes[i] = Math.floor(Math.random() * 256);
                }
                setFrequencyData(dataWithoutExtremes);
            } else if (window.audioContext && window.analyzer) {
                const data = new Uint8Array(bars + 3);
                window.analyzer.getByteFrequencyData(data);
                // Remove the lower end of the frequency data
                dataWithoutExtremes = data.slice(3, bars + 3);
                setFrequencyData(dataWithoutExtremes);
                animationFrameRef.current = requestAnimationFrame(updateFrequencyData);
                return; // Exit the function to prevent setting another interval
            } else {
                dataWithoutExtremes = new Uint8Array(bars);
                setFrequencyData(dataWithoutExtremes);
            }
        };

        if (shouldRandomize) {
            // Use setInterval when shouldRandomize is true
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
            }
            intervalRef.current = window.setInterval(updateFrequencyData, interval);
        } else {
            // Use requestAnimationFrame when shouldRandomize is false
            if (animationFrameRef.current) {
                cancelAnimationFrame(animationFrameRef.current);
            }
            animationFrameRef.current = requestAnimationFrame(updateFrequencyData);
        }

        return () => {
            if (animationFrameRef.current) {
                cancelAnimationFrame(animationFrameRef.current);
            }
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
            }
        };
    }, [running, bars, shouldRandomize, interval]);

    const barWidth = `calc((100% - ${(bars - 1) * spacing}px) / ${bars})`;

    return (
        <div
            className={classNames('aha__histogram', { active: running })}
            style={{
                backgroundColor,
                padding: padding ? padding : undefined,
                borderRadius,
                display: 'flex',
                alignItems: 'flex-end',
            }}
        >
            {Array.from({ length: bars }, (_, index) => (
                <div
                    key={index}
                    className='aha__histogram-bar'
                    style={{
                        width: barWidth,
                        height: `${(frequencyData[index] / 255) * 100}%`,
                        backgroundColor: 'currentColor',
                        marginRight: index < bars - 1 ? spacing : 0,
                        transition: shouldRandomize
                            ? `height ${interval / 1000}s ease`
                            : 'height 0.05s ease',
                    }}
                />
            ))}
        </div>
    );
};

export default Histogram;
