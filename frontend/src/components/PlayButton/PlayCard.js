import React from "react";
import classNames from "classnames";

import Histogram from "../Histogram/Histogram";

const PlayCard = ({ onClick, playing, inactive, turned }) => {
    return (
        <div className={classNames("aha__play-card anim anim-fade-in", {turned: turned}, {disabled: inactive})} onClick={onClick}>
                { turned && !inactive?
                    <Histogram 
                        className="front"
                        running={playing}
                        histogramWidth={130}
                        height={130}
                        bars={7}
                        width={10}
                        spacing={10}
                        backgroundColor="purple"
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