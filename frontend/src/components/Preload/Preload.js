import React, { useEffect, useRef, useState } from "react";

import ListenFeedback from "../Listen/ListenFeedback";
import CountDown from "../CountDown/CountDown";
// import * as audio from "../../util/audio";
import classNames from "classnames";

// Preload is an experiment screen that continues after a given time or after an audio file has been preloaded
const Preload = ({ instruction, pageTitle, duration, url, onNext }) => {
    const timeHasPassed = useRef(false);
    const audioIsAvailable = useRef(false);
    const [loaderDuration, setLoaderDuration] = useState(duration);
    const [overtime, setOvertime] = useState(false);

    const onTimePassed = () => {
        timeHasPassed.current = true;
        setLoaderDuration(0);
        setOvertime(true);
        if (audioIsAvailable.current) {
            onNext();
        }
    };



    return (
        <ListenFeedback
            className={classNames({ pulse: overtime || duration === 0 })}
            pageTitle={pageTitle}
            duration={loaderDuration}
            instruction={instruction}
            onFinish={onTimePassed}
            circleContent={duration >= 1 && <CountDown duration={duration} />}
        />
    );
};

export default Preload;
