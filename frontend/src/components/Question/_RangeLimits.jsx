import React from "react";

import { renderLabel } from "../../util/label";

const RangeLimits = ({ minVal, maxVal, labels}) => {
    return (
        <div className="limits">
            { labels ?
                <div className="labels">
                    {labels.map(label => (
                        <span>{renderLabel(label)}</span>
                    )
                    )}
                </div> :
                <div>
                    <span className="min">{renderLabel(minVal)}</span>
                    <span className="max">{renderLabel(maxVal)}</span>
                </div>
            }
        </div>
    )
};

export default RangeLimits;
