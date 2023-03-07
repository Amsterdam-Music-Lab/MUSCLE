import React from "react";
import classNames from "classnames";

import Histogram from "../Histogram/Histogram";

const PlayCard = ({ onClick, registerUserClicks, playing, inactive, turned, seen }) => {
    return (
        <div className={classNames("aha__play-card", {turned: turned}, {playing: playing}, {disabled: inactive})} onClick={event => {
            registerUserClicks(event.clientX, event.clientY);
            onClick();
        }}>
                { turned ?
                    <Histogram 
                        className="front"
                        running={playing}
                        histogramWidth={90}
                        height={90}
                        bars={5}
                        width={10}
                        spacing={10}
                        backgroundColor="purple"
                        borderRadius=".5rem"
                    />
                    :
                    <div className={classNames("back", {seen: seen})}>
                    </div>
                }
        </div>
    );
};

export default PlayCard;