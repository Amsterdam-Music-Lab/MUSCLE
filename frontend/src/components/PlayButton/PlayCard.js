import React, { useEffect, useState } from "react";
import classNames from "classnames";

import Histogram from "../Histogram/Histogram";
import Timer from "../../util/timer";

const PlayCard = ({ onClick, registerUserClicks, playing, section, onFinish, stopAudioAfter }) => {
    // automatic timer
    const startTime = 0;
    const [time, setTime] = useState(startTime);
    
    const [cardSize, setCardSize] = useState(window.innerHeight >= window.innerWidth ? window.innerWidth / 100 * 15 : window.innerHeight / 100 * 15);

    const calcCardSize = () => {
        setCardSize(window.innerHeight >= window.innerWidth ? window.innerWidth / 100 * 15 : window.innerHeight / 100 * 15);
    }

    useEffect(() => {
        window.addEventListener('resize', calcCardSize);
        return window.removeEventListener('resize', calcCardSize)
    }, [])

    useEffect(() => {
        if (!playing) {
            return;
        }

        // Create timer and return stop function
        return Timer({
            time: startTime,
            duration: stopAudioAfter,
            onTick: (t) => {
                setTime(Math.min(t, stopAudioAfter));
            },
            onFinish: () => {
                onFinish && onFinish();
            },
        });
    }, [playing, stopAudioAfter, onFinish]);
    
    return (
        <div className={classNames("aha__play-card", {turned: section.turned}, {noevents: section.noevents}, {disabled: section.inactive}, { memory: section.memory }, { lucky: section.lucky }, { nomatch: section.nomatch })} onClick={event => {
            registerUserClicks(event.clientX, event.clientY);
            onClick();
        }}>
                { section.turned ?
                    <Histogram
                        running={playing}
                        histogramWidth={cardSize}
                        height={cardSize}
                        bars={5}
                        width={cardSize/8}
                        spacing={cardSize/12}
                        marginBottom={0}
                        backgroundColor="purple"
                        borderRadius=".5rem"
                    />
                    :
                    <div className={classNames("back", {seen: section.seen})}>
                    </div>
                }
        </div>
    );
};

export default PlayCard;