import React from "react";
import classNames from "classnames";

const PlayButton = ({ onClick, className = ""}) => {
    return (
        <div
            className={classNames(
                "aha__play-button border-outside",
                "btn",
                className
            )}
            onClick={onClick}
            tabIndex="0"
            onKeyPress={(e) => {
                onClick();
            }}
        ></div>
    );
};

export default PlayButton;
