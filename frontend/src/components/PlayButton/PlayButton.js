import React, { useState } from "react";
import classNames from "classnames";

const PlayButton = ({ playSection, isPlaying, className="" }) => {

    const [clicked, setClicked] = useState(false);

    return (
        <>
        <div
            className={classNames("aha__play-button btn-blue border-outside", "btn", {
                stop: isPlaying, disabled: clicked && !isPlaying,
            },className)}
            onClick={ (playSection && !clicked) ? () => {setClicked(true); playSection(0);} : undefined}
            tabIndex="0"
            onKeyPress={(e) => {
                playSection && playSection(0)
            }}
        >
        </div>
        <div className="playbutton-spacer"></div>
        </>
    );
};

export default PlayButton;