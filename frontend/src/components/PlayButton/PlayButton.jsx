import React from "react";
import classNames from "classnames";

const PlayButton = ({ playSection, isPlaying, className = "", disabled }) => {

    return (
        <>
            <div
                className={classNames("aha__play-button btn-blue border-outside", "btn", {
                    stop: isPlaying, disabled: disabled || isPlaying
                }, className)}
                onClick={playSection && !disabled ? () => playSection(0) : undefined}
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
