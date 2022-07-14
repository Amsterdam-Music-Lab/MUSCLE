import React from "react";
import classNames from "classnames";

const PlayButton = ({ playSection, isPlaying, className="" }) => {
    return (
        <div
            className={classNames("aha__play-button border-outside", "btn", {
                stop: isPlaying,
            },className)}
            onClick={playSection ? () => playSection(0) : undefined}
            tabIndex="0"
            onKeyPress={(e) => {
                playSection(0);
            }}
        ></div>
    );
};

export default PlayButton;
