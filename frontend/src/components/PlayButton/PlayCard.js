import React, { useEffect, useState } from "react";
import classNames from "classnames";

import Histogram from "../Histogram/Histogram";
import Timer from "../../util/timer";

const PlayCard = ({ onClick, registerUserClicks, playing, section, onFinish, stopAudioAfter }) => {
    // automatic timer
    const startTime = 0;
    const [time, setTime] = useState(startTime);
    
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
        <div className={classNames("aha__play-card", {turned: section.turned}, {disabled: section.inactive})} onClick={event => {
            registerUserClicks(event.clientX, event.clientY);
            onClick();
        }}>
                { section.turned ?
                    <Histogram 
                        className="front"
                        running={playing}
                        histogramWidth={130}
                        height={130}
                        bars={7}
                        width={10}
                        spacing={10}
                        backgroundColor="purple"
                        borderRadius="1rem"
                    />
                    :
                    <img 
                        className="back"
                        src='favicon.ico' 
                        alt="card back" 
                    />
                }
        </div>
    );
};

export default PlayCard;