import React, { useEffect, useRef, useState } from 'react';
import classNames from 'classnames';

interface HistogramProps {
    bars?: number;
    spacing?: number;
    running?: boolean;
    marginLeft?: number;
    marginTop?: number;
    backgroundColor?: string;
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
    marginLeft = 0,
    marginTop = 0,
    backgroundColor = undefined,
    borderRadius = '0.15rem',
    random = false,
    interval = 100,
}) => {
    const [frequencyData, setFrequencyData] = useState<Uint8Array>(new Uint8Array(bars));

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

            if (random) {
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

        if (random) {
            // Use setInterval when random is true
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
            }
            intervalRef.current = window.setInterval(updateFrequencyData, interval);
        } else {
            // Use requestAnimationFrame when random is false
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
    }, [running, bars, random, interval]);

    const barWidth = `calc((100% - ${(bars - 1) * spacing}px) / ${bars})`;

    return (
        <div
            className={classNames('aha__histogram', { active: running })}
            style={{
                height: '100%',
                marginLeft,
                marginTop,
                backgroundColor,
                width: '100%',
                borderRadius,
                border: backgroundColor ? `10px solid ${backgroundColor}` : undefined,
                display: 'flex',
                alignItems: 'flex-start',
            }}
        >
            {Array.from({ length: bars }, (_, index) => (
                <div
                    key={index}
                    style={{
                        width: barWidth,
                        height: `${(frequencyData[index] / 255) * 100}%`,
                        backgroundColor: 'currentColor',
                        marginRight: index < bars - 1 ? spacing : 0,
                        transition: random
                            ? `height ${interval / 1000}s ease`
                            : 'height 0.05s ease',
                    }}
                />
            ))}
        </div>
    );
};

export default Histogram;
