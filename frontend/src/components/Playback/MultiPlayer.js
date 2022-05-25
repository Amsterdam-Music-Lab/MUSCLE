import React, { useRef } from "react";

import PlayerSmall from "../PlayButton/PlayerSmall";



const MultiPlayer = ({playSection, sections, instruction, playConfig}) => {
    const cancelEvents = useRef(null);

    const cancelActiveEvents = () => {
        // cancel events
        if (cancelEvents.current) {
            cancelEvents.current();
            cancelEvents.current = null;
        }
    };

    return (
        <div className="aha__multiplayer d-flex justify-content-between">
        {Object.keys(sections).map((index) => (
            <PlayerSmall onClick={() => {
                playSection(index);
            }}/>
        ))}
        </div>
    )
}
export default MultiPlayer;
