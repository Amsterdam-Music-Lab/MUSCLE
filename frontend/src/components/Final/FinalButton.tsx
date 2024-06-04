import React from "react";
import { Link, withRouter } from "react-router-dom";

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

    if (!button) {
        return null;
    }

    if (!button.link) {
        return (
            <button data-testid="button" className='btn btn-primary btn-lg' onClick={() => onNext(false)}>
                {button.text}
            </button>
        )
    }

    if (isRelativeUrl(button.link)) {
        return (
            <Link data-testid="button-link" className='btn btn-primary btn-lg' to={button.link}>
                {button.text}
            </Link>
        )
    }

    return (
        <a data-testid="button-link" className='btn btn-primary btn-lg' href={button.link} target="_blank" rel="noopener noreferrer">
            {button.text}
        </a>
    )
}

export default withRouter(FinalButton);