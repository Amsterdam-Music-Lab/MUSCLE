import React from "react";
import Histogram from "../Histogram/Histogram";
import CountDown from "../CountDown/CountDown";

const ListenCircle = ({
    duration,
    countDownRunning = true,
    histogramRunning = true
}) => {
    return (
        <>
            <CountDown duration={duration} running={countDownRunning} />
            <Histogram running={histogramRunning} />
        </>
    );
};

export default ListenCircle;
