import PlayButton from "./PlayButton/PlayButton";
import classNames from "classnames";
import PlaybackSection from "@/types/Section";

interface MultiPlayerProps {
    playSection: (section: PlaybackSection) => void;
    sections: PlaybackSection[];
    playOnce: boolean;
    extraContent?: (index: number) => JSX.Element;
}

const MultiPlayer = ({
    playSection,
    sections,
    playOnce,
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
                        onClick={() => {
                            playSection(section);
                        }}
                        disabled={
                            playOnce ? section.hasPlayed : false
                        }
                        label={
                            section.label
                        }
                        color={
                            section.color
                        }
                        playing={section.playing}
                    />
                    {section.image && (
                    <div className="image">
                        <img
                            src={section.image.link}
                            alt="PlayerImage"
                            onClick={() => {
                                playSection(section);
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
