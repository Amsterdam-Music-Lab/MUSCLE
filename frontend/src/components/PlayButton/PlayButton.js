import React, { useState } from "react";
import classNames from "classnames";

const PlayButton = ({ children, playSection, isPlaying, className="" }) => {

    const [clicked, setClicked] = useState(false);

    return (
        <div
            className={classNames("aha__play-button border-outside", "btn", {
                stop: isPlaying, disabled: clicked && !isPlaying,
            },className)}
            onClick={ (playSection && !clicked) ? () => {setClicked(true); playSection(0);} : undefined}
            tabIndex="0"
            onKeyPress={(e) => {
                playSection && playSection(0)
            }}
        >
            {children}
        </div>
    );
};

export default PlayButton;
