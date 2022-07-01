import React from "react";

import PlayerSmall from "../PlayButton/PlayerSmall";



const MultiPlayer = ({playSection, sections, playerIndex}) => {
    return (
        <div className="aha__multiplayer d-flex justify-content-between">
        {Object.keys(sections).map((index) => (
            <PlayerSmall 
                key={index} 
                onClick={() => {
                    playSection(index);
                }}
                label={index}
                playing={playerIndex === index}
            />
        ))}
        </div>
    )
}
export default MultiPlayer;
