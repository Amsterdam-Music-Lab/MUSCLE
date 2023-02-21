import React from "react";
import classNames from "classnames";

// Rank shows a decorated representation of a rank
const Rank = ({ rank }) => {
    return (
        <div
            className={classNames("aha__rank", rank.class, {
                offsetCup: rank.text,
            })}
        >
            <div className="cup" />
            <h4>{rank.text}</h4>
        </div>
    );
};

export default Rank;
