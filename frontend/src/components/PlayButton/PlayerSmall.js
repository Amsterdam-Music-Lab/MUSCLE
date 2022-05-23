import React from "react";
import PlayButton from "./PlayButton";
import classNames from "classnames";

const PlayerSmall = ({ colorClass, style, label, onClick, playing }) => (
    <div className="aha__player-small anim anim-fade-in" onClick={onClick}>
        {/* <div className={classNames("banner", "btn-" + colorClass)}></div> */}
        <div className="banner"></div>
        <h3 className="label">{label}</h3>
        <PlayButton
            className={classNames({ stop: playing })}
        />
    </div>
);

export default PlayerSmall;
