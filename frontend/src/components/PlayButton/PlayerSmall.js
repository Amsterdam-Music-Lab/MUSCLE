import React from "react";
import PlayButton from "./PlayButton";
import classNames from "classnames";

const PlayerSmall = ({ colorClass, style, label, onClick, playing, inactive, turned }) => (
    <div className={classNames("aha__player-small anim anim-fade-in",{ hasLabel: label }, {inactive: inactive}, {turned: turned})} onClick={onClick}>
        {label && <>
            <div className="banner"></div>
            <h3 className="label">{label}</h3>
        </>}
        <PlayButton
            isPlaying={playing}
        />
    </div>
);

export default PlayerSmall;
