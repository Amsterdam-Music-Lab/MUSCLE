import React from "react";
import { Link } from "react-router-dom";
import "@/components/MCGTheme/utils.scss";
import "./FinalButton.scss";

interface FinalButtonProps {
    button: {
        text: string;
        link: string;
    };
    onNext: (value: boolean) => void;
}

const isRelativeUrl = (url: string) => {
    return url && url.startsWith("/");
}

const FinalButton: React.FC<FinalButtonProps> = ({ button, onNext }) => {
    const className = "btn btn-primary btn-lg mcg-btn bg-subtle-yellow-pink"

    if (!button) {
        return null;
    }

    // If the button does not have a link, it will call the onNext function using a button click event
    if (!button.link) {
        return (
            <button data-testid="button" className={className} onClick={() => onNext(false)}>
                {button.text}
            </button>
        )
    }

    // If the button has a link, it will render a Link component if the link is a relative URL
    if (isRelativeUrl(button.link)) {
        const url = `/redirect${button.link}`

        return (
            <Link data-testid="button-link" className={className} to={url}>
                {button.text}
            </Link>
        )
    }

    // If the button has a link, it will render an anchor tag if the link is an absolute URL
    return (
        <a data-testid="button-link" className={className} href={button.link} target="_blank" rel="noopener noreferrer">
            {button.text}
        </a>
    )
}

export default FinalButton;
