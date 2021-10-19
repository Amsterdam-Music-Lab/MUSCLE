import React, { useRef } from "react";

// Listen is a base view for experiment views without user input
const Listen = ({
    instruction,
    className = "",
}) => {

    return (
        <div
            className={
                "aha__listen d-flex flex-column justify-content-center align-items-center " +
                className
            }
        >

            {/* Instruction */}
            <div className="instruction d-flex justify-content-center align-items-center">
                <h3 className="text-center">{instruction}</h3>
            </div>
        </div>
    );
};

export default Listen;
