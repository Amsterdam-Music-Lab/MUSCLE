import React, { useState, useEffect, useRef } from "react";
import { withRouter } from "react-router-dom";
import Button from "../Button/Button";
import Rank from "../Rank/Rank";
import Social from "../Social/Social";

import { URLS } from "../../config";


// FinalScore is an experiment view that shows the final scores of the experiment
// It can only be the last view of an experiment
const FinalScore = ({ rank, score, score_message, points, action_texts, show_social, onNext, history }) => {
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
        <div className="aha__final-score d-flex flex-column justify-content-center">
            <div className="text-center">
                <Rank rank={rank} />
                <h1 className="total-score title">{showScore} {points}</h1>
                <h5>{score_message}</h5>
            </div>

            <div className="d-flex justify-content-center mt-3">
                <Button
                    key={"play"}
                    className="btn-primary"
                    onClick={onNext}
                    title={action_texts.play_again}
                />
            </div>

            <Social
                renderSocial={show_social}
                score={score}
            />

            <div className=" mt-2 d-flex justify-content-center">
                <a className="home text-center" href={URLS.AMLHome}>
                    {action_texts.all_experiments}
                </a>
                <div
                    className="home text-center"
                    onClick={() => {
                        history.push(URLS.profile);
                    }}
                >
                    {action_texts.profile}
                </div>
            </div>
        </div>
    );
};

export default withRouter(FinalScore);
