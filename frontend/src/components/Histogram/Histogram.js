import React, { useEffect, useState } from "react";
import classNames from "classnames";

// Histogram with random bar movement for decoration
const Histogram = ({
    bars = 7,
    width = 6,
    spacing = 6,
    height = 40,
    interval = 100,
    running = true,
    marginLeft = 0,
    marginTop = 0,
    backgroundColor = undefined,
    histogramWidth = undefined,
    borderRadius = '0.15rem',
}) => {
    const [pulse, setPulse] = useState(true);

    useEffect(() => {
        const id = setTimeout(() => {
            setPulse(!pulse);
        }, interval);

        return () => {
            clearTimeout(id);
        };
    });

    const _bars = Array.from(Array(bars)).map((_, index) => (
        <div
            key={index}
            style={{
                width,
                height: running
                    ? Math.random() * (height - width) + width
                    : width,
                marginRight: index < bars - 1 ? spacing : 0,
            }}
        />
    ));

    return (
        <div
            className={classNames("aha__histogram", { active: running })}
            style={{ height, marginLeft, marginTop, backgroundColor, width: histogramWidth, borderRadius: borderRadius, border: backgroundColor? `10px solid purple` : undefined}}
        >
            {_bars}
        </div>
    );
};

export default Histogram;
