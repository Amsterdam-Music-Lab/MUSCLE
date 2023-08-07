import classNames from "classnames";

import Histogram from "../Histogram/Histogram";

const PlayCard = ({ onClick, registerUserClicks, playing, section }) => {
    
    return (
        <div className={classNames("aha__play-card", {turned: section.turned}, {noevents: section.noevents}, {disabled: section.inactive}, { memory: section.memory }, { lucky: section.lucky }, { nomatch: section.nomatch })} onClick={event => {
            registerUserClicks(event.clientX, event.clientY);
            onClick();
        }}>
                { section.turned ?
                    <Histogram 
                        className="front"
                        running={playing}
                        bars={5}
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