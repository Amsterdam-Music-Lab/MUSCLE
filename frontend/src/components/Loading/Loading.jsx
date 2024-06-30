import React from "react";

import Circle from "../Circle/Circle";

/**
 * Loading is an block view that shows a loading screen
 * It is normally set by code during loading of data
 */
const Loading = ({ duration = 2, loadingText }) => {
    return (
        <div className="aha__loading d-flex justify-content-center">
            <Circle
                duration={duration}
                startTime={0.1 * duration}
                running={false}
            />
            <div className="content">
                <h4>{loadingText}</h4>
            </div>
        </div>
    );
};

export default Loading;
