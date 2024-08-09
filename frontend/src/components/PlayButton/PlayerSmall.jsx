import React from "react";
import PlayButton from "./PlayButton";
import classNames from "classnames";

const PlayerSmall = ({ label, onClick, playing, disabled }) => (
    <div role="button" className={classNames("aha__player-small anim anim-fade-in", { hasLabel: label, disabled: disabled })} onClick={onClick}>
        {label && <>
            <div className="banner"></div>
            <h3 className="label">{label}</h3>
        </>}
        <PlayButton
            isPlaying={playing}
            blocked={disabled}
        />
    </div>
);

export default PlayerSmall;
