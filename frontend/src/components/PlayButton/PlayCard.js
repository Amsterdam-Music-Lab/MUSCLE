import classNames from "classnames";

import Histogram from "../Histogram/Histogram";
import { MATCHINGPAIRS } from "components/Playback/Playback";

const PlayCard = ({ onClick, registerUserClicks, playing, section, view }) => {

    return (
        <div className={classNames("aha__play-card", { turned: section.turned }, { noevents: section.noevents }, { disabled: section.inactive }, { memory: section.memory }, { lucky: section.lucky }, { nomatch: section.nomatch })} onClick={event => {
            registerUserClicks(event.clientX, event.clientY);
            onClick();
        }}>
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
                        <img src={section.url} alt={section.name} />
                    </div>
                :
                <div className={classNames("back", { seen: section.seen })}>
                </div>
            }
        </div>
    );
};

export default PlayCard;
