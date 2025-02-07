import classNames from "classnames";

import Histogram from "../Histogram/Histogram";
import { API_ROOT } from "@/config";
import { Card } from "@/types/Section";

interface PlayCardProps {
    onClick: () => void;
    registerUserClicks: (x: number, y: number) => void;
    playing: boolean;
    section: Card;
    view: string;
    showAnimation: boolean;
}

const PlayCard = ({ onClick, registerUserClicks, playing, section, view, showAnimation }: PlayCardProps) => {
    const getImgSrc = (url: string) => {
        if (url.startsWith("http")) {
            return url;
        }
        return API_ROOT + url;
    }
    const matchClass = showAnimation ? section.matchClass : '';

    const histogramBars = showAnimation ? 5 : 0;

    return (
        <div
            data-testid="play-card"
            className={
                classNames(
                    "aha__play-card",
                    matchClass,
                    { turned: section.turned },
                    { noevents: section.noevents },
                    { disabled: section.inactive },
                )
            }
            onClick={event => {
                registerUserClicks(event.clientX, event.clientY);
                onClick();
            }}
            role="button"
        >
            {section.turned ?
                view === 'visual' ?
                    <div
                        data-testid="front"
                        className="front front--visual"
                    >
                        <img src={getImgSrc(section.url)} alt={section.name} />
                    </div>
                    :
                    <Histogram
                        running={playing}
                        bars={histogramBars}
                        backgroundColor="purple"
                        borderRadius=".5rem"
                        random={true}
                        interval={200}
                    />
                :
                <div
                    data-testid="back"
                    className={classNames("back", { seen: section.seen })}
                >
                    {/* TODO: Remove this before merging PR */}
                    <span style={{ margin: '1rem' }}>
                        {section.group}
                    </span>
                </div>
            }
        </div>
    );
};

export default PlayCard;
