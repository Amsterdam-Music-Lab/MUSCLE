import React from "react";

import PlayerSmall from "../PlayButton/PlayerSmall";



const MultiPlayer = ({playSection, sections, instruction, playConfig}) => {

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
