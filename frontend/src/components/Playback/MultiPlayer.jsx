import React from "react";
import PlayerSmall from "../PlayButton/PlayerSmall";
import classNames from "classnames";

const MultiPlayer = ({
    playSection,
    sections,
    playerIndex,
    labels,
    disabledPlayers,
    extraContent,
    style,
}) => {
    return (
        <div
            className={classNames(
                "aha__multiplayer d-flex justify-content-around",
                "player-count-" + sections.length,
                style?.root
            )}
        >
            {Object.keys(sections).map((index) => (
                <div className="player-wrapper" key={index}>
                    <PlayerSmall
                        onClick={() => {
                            playSection(index);
                        }}
                        disabled={
                            Array.isArray(disabledPlayers) &&
                            disabledPlayers.includes(parseInt(index))
                        }
                        label={
                            labels? labels[index] : ""
                        }
                        playing={playerIndex === index}
                    />
                    {extraContent && extraContent(index)}
                </div>)
            )}
        </div>
    );
};

export default MultiPlayer;
