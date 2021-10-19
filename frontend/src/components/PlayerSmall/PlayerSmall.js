import React from "react";
import PlayButton from "../PlayButton/PlayButton";
import classNames from "classnames";

const PlayerSmall = ({ colorClass, label, onClick, playing }) => (
    <div className="aha__player-small anim anim-fade-in" onClick={onClick}>
        <div className={classNames("banner", "btn-" + colorClass)}></div>
        <h3 className="label">{label}</h3>
        <PlayButton
            colorClass={colorClass}
            className={classNames({ stop: playing })}
        />
    </div>
);

export default PlayerSmall;
