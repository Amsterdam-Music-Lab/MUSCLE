import React from "react";
import classNames from "classnames";

import Histogram from "../Histogram/Histogram";

const PlayCard = ({ onClick, registerUserClicks, playing, inactive, turned }) => {
    return (
        <div className={classNames("aha__play-card", {turned: turned}, {disabled: inactive})} onClick={event => {
            registerUserClicks(event.clientX, event.clientY);
            onClick();
        }}>
                { turned ?
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