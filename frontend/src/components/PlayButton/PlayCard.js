import classNames from "classnames";

import Histogram from "../Histogram/Histogram";
import { MEDIA_ROOT } from "../../config";
const PlayCard = ({ onClick, registerUserClicks, playing, section }) => {

    // preload the section (temporary solution for ICMPC)
    const audioBuffer = document.createElement("audio");
    audioBuffer.id = `buffer-${section.id}`;    
    audioBuffer.src = MEDIA_ROOT + section.url;
    audioBuffer.crossorigin = "use-credentials";
    audioBuffer.disableRemotePlayback = true;
    audioBuffer.style.display = "none";

    // Required for Firefox to trigger canplaythrough event
    audioBuffer.preload = "auto";

    // Required for Safari/iOS
    audioBuffer.load();

    // Add it to the page
    document.body.appendChild(audioBuffer);
    
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