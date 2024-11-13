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
    random?: boolean; // Added the 'random' prop
}

const Histogram: React.FC<HistogramProps> = ({
    bars = 8,
    spacing = 4,
    running = true,
    marginLeft = 0,
    marginTop = 0,
    backgroundColor = undefined,
    borderRadius = '0.15rem',
    random = false, // Default value set to false
}) => {
    const [frequencyData, setFrequencyData] = useState<Uint8Array>(new Uint8Array(bars));

    const requestRef = useRef<number>();

    useEffect(() => {
        if (!running) {
            if (requestRef.current) {
                const emptyHistogram = new Uint8Array(bars);
                setFrequencyData(emptyHistogram);
                cancelAnimationFrame(requestRef.current);
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
            requestRef.current = requestAnimationFrame(updateFrequencyData);
        };

        requestRef.current = requestAnimationFrame(updateFrequencyData);

        return () => {
            if (requestRef.current) {
                cancelAnimationFrame(requestRef.current);
            }
        };
    }, [running, bars, random]); // Added 'random' to dependency array

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
                        transition: 'height 0.05s ease',
                    }}
                />
            ))}
        </div>
    );
};

export default Histogram;
