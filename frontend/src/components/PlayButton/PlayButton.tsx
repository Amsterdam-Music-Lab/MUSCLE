import classNames from "classnames";

interface PlayButtonProps {
    playSection?: (section: number) => void;
    isPlaying: boolean;
    className?: string;
    disabled?: boolean;
}

const PlayButton = ({ playSection, isPlaying, className = "", disabled }: PlayButtonProps) => {

    return (
        <>
            <div
                className={classNames("aha__play-button btn-blue border-outside", "btn", {
                    stop: isPlaying, disabled: disabled || isPlaying
                }, className)}
                role="button"
                onClick={playSection && !disabled ? () => playSection(0) : undefined}
                tabIndex={0}
                onKeyDown={playSection && !disabled ? () => playSection(0) : undefined}
            >
            </div>
            <div className="playbutton-spacer"></div>
        </>
    );
};

export default PlayButton;
