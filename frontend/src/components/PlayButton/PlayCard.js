import classNames from "classnames";

import Histogram from "../Histogram/Histogram";

const PlayCard = ({ onClick, registerUserClicks, playing, section }) => {

    const cardSize = window.innerHeight >= window.innerWidth ? window.innerWidth / 100 * 18 : window.innerHeight / 100 * 18;
    
    return (
        <div className={classNames("aha__play-card", {turned: section.turned}, {noevents: section.noevents}, {disabled: section.inactive}, { memory: section.memory }, { lucky: section.lucky }, { nomatch: section.nomatch })} onClick={event => {
            registerUserClicks(event.clientX, event.clientY);
            onClick();
        }}>
                { section.turned ?
                    <Histogram
                        running={playing}
                        histogramWidth={cardSize}
                        height={cardSize}
                        bars={5}
                        width={cardSize/8}
                        spacing={cardSize/12}
                        marginBottom={0}
                        backgroundColor="purple"
                        borderRadius=".5rem"
                    />
                    :
                    <div className={classNames("back", {seen: section.seen})}>
                    </div>
                }
        </div>
    );
};

export default PlayCard;