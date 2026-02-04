import React, { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import classNames from "classnames";

import { audioInitialized } from "../../util/audio";
import { styleButton } from "@/util/stylingHelpers";
import useBoundStore from "@/util/stores";


interface ButtonProps {
    label: string;
    color?: string;
    link?: string;
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
    label,
    onClick,
    className = "",
    padding = "px-4",
    style = {},
    disabled = false,
    value = "",
    clickOnce = true,
    color = 'colorPrimary',
    link,
}: ButtonProps) => {
    const clicked = useRef(false);
    const theme = useBoundStore((state) => state.theme);
    const colorValue = theme? theme[color] : '#fabbacc';

    useEffect(() => {
        // reset clicked ref on rerender
        clicked.current = false;
    }, [value, label, link, clickOnce, disabled, color]);

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
    
    const isRelativeUrl = (url: string) => {
        return url && url.startsWith("/");
    }

    const buttonIsLink = !onClick && link;

    if (buttonIsLink) {
        
         // If the button has a relative link, it will render a Link component
        if (isRelativeUrl(link)) {
            const url = `/redirect${link}`

            return (
                <Link data-testid="button-link" className='btn btn-lg' css={styleButton(colorValue)} to={url}>
                    {label}
                </Link>
            )
        }

        // If the button has an absolute link, it will render an anchor tag
        return (
            <a data-testid="button-link" className='btn btn-lg' href={link} css={styleButton(colorValue)} target="_blank" rel="noopener noreferrer">
                {label}
            </a>
        )
    } else {
        return (
            <button
                className={classNames({ disabled }, className, padding, "aha__button btn btn-lg")}
                onClick={(e) => {
                    clickOnceGuard();
                }}
                disabled={disabled}
                style={style}
                css={styleButton(colorValue)}
                tabIndex={0}
                onKeyUp={(e) => {
                    clickOnceGuard();
                }}
                type="button"
                {...touchEvent}
            >
                {label}
            </button>
        );
    }
};

export default Button;
