import classNames from "classnames";

import Histogram from "../Histogram/Histogram";
import { MATCHINGPAIRS } from "components/Playback/Playback";
import { API_ROOT } from "config";

const PlayCard = ({ onClick, registerUserClicks, playing, section, view }) => {

    const getImgSrc = (url) => {
        if (url.startsWith("http")) {
            return url;
        }
        return API_ROOT + url;
    }

    return (
        <div
            data-testid="play-card"
            className={
                classNames(
                    "aha__play-card",
                    { turned: section.turned },
                    { noevents: section.noevents },
                    { disabled: section.inactive },
                    { memory: section.memory },
                    { lucky: section.lucky },
                    { nomatch: section.nomatch })
            }
            onClick={event => {
                registerUserClicks(event.clientX, event.clientY);
                onClick();
            }}
            role="button"
        >
            {section.turned ?
                view === MATCHINGPAIRS ?
                    <Histogram
                        className="front"
                        running={playing}
                        bars={5}
                        marginBottom={0}
                        backgroundColor="purple"
                        borderRadius=".5rem"
                    />
                    : <div className="front front--visual">
                        <img src={getImgSrc(section.url)} alt={section.name} />
                    </div>
                :
                <div className={classNames("back", { seen: section.seen })}>
                </div>
            }
        </div>
    );
};

export default PlayCard;
