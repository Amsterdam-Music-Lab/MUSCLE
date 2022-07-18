import React, { useEffect, useState } from "react";

import Button from "../Button/Button";

// Info is an experiment view that shows the Info text, and handles agreement/stop actions
const Info = ({ heading, body, buttonLabel, buttonLink, onNext }) => {
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

    // Show Info
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
            />

            {buttonLabel && (
                <div className="buttons d-flex justify-content-center pt-3">
                    {buttonLink ? (
                        <a
                            className="btn btn-primary"
                            href={buttonLink}
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            {buttonLabel}
                        </a>
                    ) : (
                        <Button
                            className="btn-primary"
                            onClick={onNext}
                            title={buttonLabel}
                        />
                    )}
                </div>
            )}
        </div>
    );
};

const getMaxHeight = () => {
    // Calculate height for Info text to prevent overlapping browser chrome
    const height = document.documentElement?.clientHeight || window.innerHeight;

    const width = document.documentElement?.clientWidth || window.innerWidth;

    const correction = width > 720 ? 280 : 250;

    return height - correction;
};

export default Info;
