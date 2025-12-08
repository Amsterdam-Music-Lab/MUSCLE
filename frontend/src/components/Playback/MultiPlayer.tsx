import PlayButton from "./PlayButton/PlayButton";
import classNames from "classnames";
import PlaybackSection from "@/types/Section";

interface MultiPlayerProps {
    playSection: (index: number) => void;
    hasPlayed: number[];
    sections: PlaybackSection[];
    playOnce?: boolean;
    playing: number;
}

const MultiPlayer = ({
    playSection,
    sections,
    playOnce=false,
    hasPlayed=[],
    playing
}: MultiPlayerProps) => {
    return (
        <div
            data-testid="multiplayer"
            className={classNames(
                "aha__multiplayer d-flex justify-content-around",
                "player-count-" + sections.length,
            )}
        >
            {sections.map((section, index) => (
                <div className="player-wrapper" key={index}>
                    <PlayButton
                        playSection={playSection}
                        disabled={
                            playOnce ? hasPlayed.includes(index) : false
                        }
                        playIndex={index}
                        section={section}
                        isPlaying={playing===index}
                    />
                    {section.image && (
                    <div className="image">
                        <img
                            src={section.image.link}
                            alt={section.image.label}
                            onClick={() => {
                                playSection(index);
                            }}
                        />
                        {section.image.label && (
                            <span>{section.image.label}</span>
                        )}
                    </div>
                    )}
                </div>)
            )}
        </div>
    );
};

export default MultiPlayer;
