import React from "react";
import classNames from "classnames";

const PlayButton = ({ playSection, className = "", colorClass = "pink" }) => {
    return (
        <div
            className={classNames(
                "aha__play-button border-outside",
                "btn",
                // "btn-" + colorClass,
                className
            )}
            onClick={() => playSection(0)}
            tabIndex="0"
            onKeyPress={(e) => {
                playSection(0);
            }}
        ></div>
    );
};

export default PlayButton;
