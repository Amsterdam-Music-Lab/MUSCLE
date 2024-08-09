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
    extraContent?: (index: string) => React.ReactNode;
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
                            playSection(parseInt(index));
                        }}
                        disabled={
                            Array.isArray(disabledPlayers) &&
                            disabledPlayers.includes(parseInt(index))
                        }
                        label={
                            labels ? labels[index] : ""
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
