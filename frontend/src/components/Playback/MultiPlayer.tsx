import React from "react";
import PlayerSmall from "../PlayButton/PlayerSmall";
import classNames from "classnames";
import { PlaybackArgs } from "@/types/Playback";
import Section from "@/types/Section";

interface MultiPlayerProps {
    playSection: (index: number) => void;
    sections: Section[];
    playerIndex: string;
    labels?: PlaybackArgs["labels"];
    disabledPlayers?: number[];
    extraContent?: (index: number) => JSX.Element;
    style?: PlaybackArgs["style"];
}

const MultiPlayer = ({
    playSection,
    sections,
    playerIndex,
    labels,
    disabledPlayers,
    extraContent,
    style,
}: MultiPlayerProps) => {
    return (
        <div
            data-testid="multiplayer"
            className={classNames(
                "aha__multiplayer d-flex justify-content-around",
                "player-count-" + sections.length,
                style
            )}
        >
            {sections.map((_section, index) => (
                <div className="player-wrapper" key={index}>
                    <PlayerSmall
                        onClick={() => {
                            playSection(index);
                        }}
                        disabled={
                            Array.isArray(disabledPlayers) &&
                            disabledPlayers.includes(index)
                        }
                        label={
                            labels ? labels[index] : ""
                        }
                        playing={parseInt(playerIndex) === index}
                    />
                    {extraContent && extraContent(index)}
                </div>)
            )}
        </div>
    );
};

export default MultiPlayer;
