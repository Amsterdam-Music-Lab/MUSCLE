import React, { useState, useEffect, useRef } from "react";
import { withRouter } from "react-router-dom";

// FinalScore is an experiment view that shows the final scores of the experiment
// It can only be the last view of an experiment
const Final= ({ score, score_message, onNext, history }) => {
    const [showScore, setShowScore] = useState(0);

    // Use a ref to prevent doing multiple increments
    // when the render is skipped
    const scoreValue = useRef(0);

    useEffect(() => {
        if (score === 0) {
            return;
        }

        const interval = Math.abs(2500 / score);

        const id = setTimeout(() => {
            if (score !== scoreValue.current) {
                // lower
                if (scoreValue.current < score) {
                    scoreValue.current += 1;
                    setShowScore(scoreValue.current);
                } else {
                    scoreValue.current -= 1;
                    setShowScore(scoreValue.current);
                }
            }
        }, interval);

        return () => {
            clearTimeout(id);
        };
    }, [score, showScore]);

    return (
        <div className="aha__final d-flex flex-column justify-content-center">
            <div className="text-center">
                <h5>{score_message}</h5>
            </div>
        </div>
    );
};

export default withRouter(Final);
