import classNames from "classnames";

import Histogram from "../Histogram/Histogram";
import { API_ROOT } from "@/config";
import { Card } from "@/types/Section";
import useBoundStore from "@/util/stores";

interface PlayCardProps {
    onClick: () => void;
    registerUserClicks: (x: number, y: number) => void;
    playing: boolean;
    section: Card;
    view: string;
    showAnimation: boolean;
}

const PlayCard = ({ onClick, registerUserClicks, section, view, showAnimation }: PlayCardProps) => {
    const theme = useBoundStore((state) => state.theme);
    const cardColor = section.color || 'colorPrimary';
    const cardColorValue = `hsl(from ${theme[cardColor]} h s 35%)`;
    
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
                section.playMethod === 'NOAUDIO' ?
                    <div
                        data-testid="front"
                        className="front front--visual"
                    >
                        <img src={getImgSrc(section.link)} alt={section.label} />
                    </div>
                    :
                    <Histogram
                        running={section.playing}
                        bars={histogramBars}
                        backgroundColor={cardColorValue}
                        borderRadius=".5rem"
                        random={true}
                        interval={200}
                    />
                :
                <div
                    data-testid="back"
                    className={classNames("back", { seen: section.seen })}
                >
                </div>
            }
        </div>
    );
};

export default PlayCard;
