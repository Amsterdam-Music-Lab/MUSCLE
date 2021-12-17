import React, { useRef } from "react";
import classnames from "classnames";
import { audioInitialized } from "../../util/audio";

// Button is a button that can only be clicked one time
const Button = ({
    title,
    onClick,
    className = "",
    padding = "px-4",
    style = {},
    active = true,
    value = ""
}) => {
    const clicked = useRef(false);

    // Only handle the first click
    const clickOnce = () => {
        if (!active || clicked.current) {
            return;
        }
        clicked.current = true;
        onClick(value);
    };

    // Only support touch events as the audio is initialized
    // Otherwise iOS-Safari users can start the player (by a touchstart)
    // Without the browser having registered any user interaction (e.g. click)
    const touchEvent = audioInitialized ? { onTouchStart: clickOnce } : {};

    return (
        <div
            className={classnames(
                { active },
                className,
                padding,
                "aha__button btn btn-lg"
            )}
            onClick={(e) => {
                clickOnce();
            }}
            style={style}
            tabIndex="0"
            onKeyPress={(e) => {
                clickOnce();
            }}
            {...touchEvent}
            disabled={!active}
        >
            {title}
        </div>
    );
};

export default Button;
