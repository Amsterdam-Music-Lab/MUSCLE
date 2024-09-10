import PlayButton from "./PlayButton";
import classNames from "classnames";

interface PlayerSmallProps {
    label?: string;
    onClick: () => void;
    playing: boolean;
    disabled?: boolean;
}

const PlayerSmall = ({ label, onClick, playing, disabled }: PlayerSmallProps) => {

    const classes = classNames(
        "aha__player-small anim anim-fade-in",
        { hasLabel: label, disabled: disabled }
    );

    return (
        <div
            data-testid="player-small"
            role="button"
            className={classes}
            onClick={onClick}>
            {label && <>
                <div className="banner"></div>
                <h3 className="label">{label}</h3>
            </>}
            <PlayButton
                isPlaying={playing}
                disabled={disabled}
            />
        </div>
    )
};

export default PlayerSmall;
