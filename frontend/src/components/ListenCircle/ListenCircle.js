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
            <div className="aha__histogram-container">
                <Histogram running={histogramRunning} />
            </div>
        </>
    );
};

export default ListenCircle;
