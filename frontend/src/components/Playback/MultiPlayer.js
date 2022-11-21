import React from "react";
import PlayerSmall from "../PlayButton/PlayerSmall";
import PlayCard from "../PlayButton/PlayCard";
import classNames from "classnames";
import { romanNumeral } from "../../util/roman";

export const LABEL_NUMERIC = 'NUMERIC';
export const LABEL_ALPHABETIC = 'ALPHABETIC';
export const LABEL_ROMAN = 'ROMAN';

const MultiPlayer = ({playSection, registerUserClicks, sections, playerIndex, playConfig}) => {
    return (
        <div className={classNames("aha__multiplayer d-flex justify-content-around", "player-count-" + sections.length)}>
        {Object.keys(sections).map((index) => (
            // <PlayerSmall 
            //     key={index} 
            //     onClick={() => {
            //         playSection(index);
            //     }}
            //     label={playConfig.label_style ? getLabel(index, playConfig.label_style) : ''}
            //     playing={playerIndex === index}
            //     inactive={sections[index].inactive}
            //     turned={sections[index].turned}
            // />
            <PlayCard 
                key={index}
                onClick={()=> playSection(index)}
                registerUserClicks={registerUserClicks}
                playing={playerIndex === index}
                inactive={sections[index].inactive}
                turned={sections[index].turned}
            />
        ))}
        </div>
    )
}

const getLabel = (index, labelStyle) =>{
    index = parseInt(index)

    switch(labelStyle){
        case LABEL_NUMERIC:
            return parseInt(index) + 1;
        case LABEL_ALPHABETIC:
            return String.fromCharCode(65+index)
        case LABEL_ROMAN:
            return romanNumeral(index+1);
        default:
            return '';
    }
}

export default MultiPlayer;
