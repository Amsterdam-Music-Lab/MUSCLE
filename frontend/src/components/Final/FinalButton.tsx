import { styleButton } from "@/util/stylingHelpers";
import React from "react";
import { Link } from "react-router-dom";

import IButton from "@/types/Button";

interface FinalButtonProps {
    button: IButton;
    onNext: (value: boolean) => void;
}

const isRelativeUrl = (url: string) => {
    return url && url.startsWith("/");
}

const FinalButton: React.FC<FinalButtonProps> = ({ button, onNext }) => {

    if (!button) {
        return null;
    }

    // If the button does not have a link, it will call the onNext function using a button click event
    if (!button.link) {
        return (
            <button data-testid="button" className='btn btn-primary btn-lg' onClick={() => onNext(false)}>
                {button.label}
            </button>
        )
    }

    // If the button has a link, it will render a Link component if the link is a relative URL
    if (isRelativeUrl(button.link)) {
        const url = `/redirect${button.link}`

        return (
            <Link data-testid="button-link" className='btn btn-lg' css={styleButton(button.color)} to={url}>
                {button.label}
            </Link>
        )
    }

    // If the button has a link, it will render an anchor tag if the link is an absolute URL
    return (
        <a data-testid="button-link" className='btn btn-lg' href={button.link} css={styleButton(button.color)} target="_blank" rel="noopener noreferrer">
            {button.label}
        </a>
    )
}

export default FinalButton;
