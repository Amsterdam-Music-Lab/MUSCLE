import classNames from "classnames";

import PlaybackSection from "@/types/Section";
import useBoundStore from "@/util/stores";
import { styleButton } from "@/util/stylingHelpers";

interface PlayButtonProps {
    playSection?: (index: number) => void;
    playIndex: number;
    className?: string;
    disabled?: boolean;
    isPlaying: boolean;
    section: PlaybackSection
}

const PlayButton = ({ playSection, className = "", disabled, section, isPlaying, playIndex}: PlayButtonProps) => {

    const theme = useBoundStore((state) => state.theme);
    const color = section.color || 'colorNeutral2';
    const colorValue = theme? theme[color] : '#fabbacc';
        

    return (
        <>
            <div
                className={classNames("aha__play-button border-outside", "btn", {
                    stop: isPlaying, disabled: disabled || isPlaying
                }, className)}
                role="button"
                css={styleButton(colorValue)}
                onClick={playSection && !disabled ? () => playSection(playIndex) : undefined}
                tabIndex={0}
                onKeyDown={playSection && !disabled ? () => playSection(playIndex) : undefined}
            >
            </div>
            {/* <div className="mask"></div> */}
            {section.label && <>
                <center>
                    <div className="banner" style={{backgroundColor: colorValue}}></div>
                    <h3 className="label">{section.label}</h3>
                </center>
            </>}
        </>
    );
};

export default PlayButton;
