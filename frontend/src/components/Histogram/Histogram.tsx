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
    interval?: number; // Added the 'interval' prop
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
    interval = 10, // Default value set to 100 milliseconds
}) => {
    const [frequencyData, setFrequencyData] = useState<Uint8Array>(new Uint8Array(bars));

    const intervalRef = useRef<number>();
    const lastUpdateTimeRef = useRef<number>(0);

    useEffect(() => {
        if (!running) {
            if (intervalRef.current) {
                const emptyHistogram = new Uint8Array(bars);
                setFrequencyData(emptyHistogram);
                clearInterval(intervalRef.current);
            }
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
            } else if (window.audioContext && window.analyzer) {
                const data = new Uint8Array(bars + 3);
                window.analyzer.getByteFrequencyData(data);
                // Remove the lower end of the frequency data
                dataWithoutExtremes = data.slice(3, bars + 3);
            } else {
                dataWithoutExtremes = new Uint8Array(bars);
            }

            setFrequencyData(dataWithoutExtremes);
        };

        // Clear any existing interval
        if (intervalRef.current) {
            clearInterval(intervalRef.current);
        }

        // Set up the interval to update frequency data
        intervalRef.current = window.setInterval(updateFrequencyData, interval);

        return () => {
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
                        transition: `height ${interval / 1000}s ease`,
                    }}
                />
            ))}
        </div>
    );
};

export default Histogram;
