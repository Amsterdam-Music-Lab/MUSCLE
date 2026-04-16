import { useState } from "react";
import classNames from "classnames";

import PlaybackSection from "@/types/Section";
import useBoundStore from "@/util/stores";
import { styleButton } from "@/util/stylingHelpers";

interface PlayButtonProps {
    onClick: () => void;
    className?: string;
    disabled?: boolean;
    isPlaying: boolean
    section: PlaybackSection
}

const SectionLabel = ({ label, colorValue, hasImage }: { label: string; colorValue: string; hasImage: boolean; }) => (
    <div className={classNames("section-label", {"has-image": hasImage})}>
        <div className={classNames("banner", {"has-image": hasImage})} style={{backgroundColor: colorValue}}>
            <h3 className="label">{label}</h3>
        </div>
    </div>
);

const PlayButton = ({ onClick, className = "", disabled, isPlaying, section }: PlayButtonProps) => {

    const theme = useBoundStore((state) => state.theme);
    const color = section.color || 'colorNeutral2';
    const colorValue = theme? theme[color] : '#fabbacc';
    const hasLabel = section.label;

    const playSection = () => {
        if (!disabled) {
            return onClick();
        }
    }

    return (
        <div className={classNames("play-button-container", { "has-image": section.image })}>
            <div
                className={classNames("aha__play-button border-outside", "btn", {
                    stop: isPlaying, disabled: disabled
                }, className)}
                role="button"
                css={styleButton(colorValue)}
                onClick={playSection}
                tabIndex={0}
                onKeyDown={playSection}
            >
            </div>
            {hasLabel && <SectionLabel label={section.label} colorValue={colorValue} hasImage={section.image}/>}
        </div>
    );
};

export default PlayButton;
