import React from "react";
import classnames from "classnames";

// Rank shows a decorated representation of a rank
const Rank = ({ rank }) => {
    return (
        <div className={classnames("aha__rank", rank.class)}>
            <div className="cup" />
            <h4>{rank.text}</h4>
        </div>
    );
};

export default Rank;
