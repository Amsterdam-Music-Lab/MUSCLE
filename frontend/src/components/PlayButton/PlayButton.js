import React, { useState } from "react";
import classNames from "classnames";

const PlayButton = ({ playSection, isPlaying, className="" }) => {

    const [clicked, setClicked] = useState(false);

    return (
        <div
            className={classNames("aha__play-button border-outside", "btn", "btn-gray", {
                stop: isPlaying, disabled: clicked && !isPlaying,
            },className)}
            onClick={ (playSection && !clicked) ? () => {setClicked(true); playSection(0);} : undefined}
            tabIndex="0"
            onKeyPress={(e) => {
                playSection(0);
            }}
        ></div>
    );
};

export default PlayButton;
