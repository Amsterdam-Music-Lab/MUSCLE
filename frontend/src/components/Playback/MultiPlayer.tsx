import classNames from "classnames";

import PlayButton from "./PlayButton";
import PlaybackSection from "@/types/Section";

interface MultiPlayerProps {
    sections: PlaybackSection[];
    playOnce?: boolean;
    playSection: (index: number) => void;
}

const MultiPlayer = ({
    playSection,
    sections,
    playOnce=false,
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
                        onClick={() => playSection(index)}
                        isPlaying={section.playing}
                        disabled={
                            playOnce ? section.hasPlayed : false
                        }
                        section={section}
                    />
                    {section.image && (
                    <div className="image">
                        <img
                            src={section.image.link}
                            alt={section.image.label}
                            onClick={() => playSection(index)}
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
