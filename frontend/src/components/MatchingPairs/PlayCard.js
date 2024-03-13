import classNames from "classnames";

import Histogram from "../Histogram/Histogram";
import { API_ROOT } from "@/config";

const PlayCard = ({ onClick, registerUserClicks, playing, section, view, showAnimation }) => {
    const getImgSrc = (url) => {
        if (url.startsWith("http")) {
            return url;
        }
        return API_ROOT + url;
    }
    const matchClass = section.matchClass;

    const histogramBars = showAnimation ? 5 : 0;

    console.log("MATCH CLASS", matchClass)
   
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
                        marginBottom={0}
                        backgroundColor="purple"
                        borderRadius=".5rem"
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
