import { useEffect, useState } from "react";

import Button from "../Button/Button";
import { Info as InfoAction } from "@/types/Action";
import IButton from "@/types/Button";

export interface InfoProps extends InfoAction {
    onNext?: () => void;
    button: IButton;
}

/** Info is a block view that shows the Info text, and handles agreement/stop actions */
const Info = ({ heading, body, button, onNext }: InfoProps) => {
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

            {button && (
                <div className="buttons d-flex justify-content-center pt-3">
                    <Button
                        {...button}
                        onClick={onNext}
                    />
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
