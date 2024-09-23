import { useEffect, useState } from "react";

import Button from "../Button/Button";

export interface InfoProps {
    heading?: string;
    body: string | TrustedHTML;
    button_label?: string;
    button_link?: string;
    onNext?: () => void;
}

/** Info is a block view that shows the Info text, and handles agreement/stop actions */
const Info = ({ heading, body, button_label, button_link, onNext }: InfoProps) => {
    const [maxHeight, setMaxHeight] = useState(getMaxHeight());

    useEffect(() => {
        const onResize = () => {
            setMaxHeight(getMaxHeight());
        };
        window.addEventListener("resize", onResize);

        return () => {
            window.removeEventListener("resize", onResize);
        };
    }, []);

    return (
        <div className="aha__info">
            {heading && (
                <div className="aha__info-header d-flex">
                    <div className="flex-fill">
                        <h3 className="title">{heading}</h3>
                    </div>
                </div>
            )}

            <div
                className="info-body"
                style={{ maxHeight }}
                dangerouslySetInnerHTML={{ __html: body }}
                data-testid="info-body"
            />

            {button_label && (
                <div className="buttons d-flex justify-content-center pt-3">
                    {button_link ? (
                        <a
                            className="btn btn-primary"
                            href={button_link}
                            target={button_link.startsWith("http") ? "_blank" : undefined}
                            rel="noopener noreferrer"
                        >
                            {button_label}
                        </a>
                    ) : onNext ? (
                        <Button
                            className="btn-primary"
                            onClick={onNext}
                            title={button_label}
                        />
                    ) : null
                    }
                </div>
            )}
        </div>
    );
};

/** Calculate height for Info text to prevent overlapping browser chrome */
const getMaxHeight = () => {
    const height = document.documentElement?.clientHeight || window.innerHeight;

    const width = document.documentElement?.clientWidth || window.innerWidth;

    const correction = width > 720 ? 280 : 250;

    return height - correction;
};

export default Info;
