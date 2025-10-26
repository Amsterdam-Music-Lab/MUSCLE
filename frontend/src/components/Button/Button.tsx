import React, { useRef } from "react";
import classNames from "classnames";
import { audioInitialized } from "../../util/audio";


interface ButtonProps {
    title: string;
    onClick: (value?: string | boolean) => void;
    className?: string;
    padding?: string;
    style?: React.CSSProperties;
    disabled?: boolean;
    value?: string;
    clickOnce?: boolean;
}

// Button is a button that can only be clicked one time by default
const Button = ({
    title,
    onClick,
    className = "",
    padding = "px-4",
    style = {},
    disabled = false,
    value = "",
    clickOnce = true,
}: ButtonProps) => {
    const clicked = useRef(false);

    // Only handle the first click
    const clickOnceGuard = () => {

        if (!clickOnce) {
            return onClick(value);
        }

        if (disabled || clicked.current) {
            return;
        }
        clicked.current = true;
        onClick(value);
    };

    // Only support touch events as the audio is initialized
    // Otherwise iOS-Safari users can start the player (by a touchstart)
    // Without the browser having registered any user interaction (e.g. click)
    const touchEvent = audioInitialized
        ? {
            onTouchStart: (e: React.TouchEvent) => {
                e.stopPropagation();
                clickOnceGuard();
                return false;
            },
        }
        : {};

    return (
        <button
            className={classNames({ disabled }, className, padding, "aha__button btn btn-lg")}
            onClick={(e) => {
                clickOnceGuard();
            }}
            disabled={disabled}
            style={style}
            tabIndex={0}
            onKeyPress={(e) => {
                clickOnceGuard();
            }}
            type="button"
            {...touchEvent}
        >
            {title}
        </button>
    );
};

export default Button;
