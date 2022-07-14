import React, { useState, useEffect, useRef } from "react";
import classNames from "classnames";
import Circle from "../Circle/Circle";
import Button from "../Button/Button";

// Score is an experiment view that shows an intermediate and total score
const Score = ({
    last_song,
    score,
    score_message,
    total_score,
    texts,
    icon,
    feedback,
    timer,
    onNext,
}) => {
    const [showScore, setShowScore] = useState(0);
    // Use a ref to prevent doing multiple increments
    // when the render is skipped
    const scoreValue = useRef(0);

    useEffect(() => {
        const id = setTimeout(() => {
            if (score !== scoreValue.current) {
                if (scoreValue.current < score) {
                    scoreValue.current += 1;
                    setShowScore(scoreValue.current);
                } 
                if (scoreValue.current > score){
                    scoreValue.current -= 1;
                    setShowScore(scoreValue.current);
                }
            }
        }, 50);

        return () => {
            window.clearTimeout(id);
        };
    }, [score,showScore]);

    useEffect(() => {
        let id = -1;
        if (timer) {
            id = setTimeout(() => {
                onNext();
            }, timer * 1000);
        }

        return () => {
            if (timer) {
                clearTimeout(id);
            }
        };
    }, [timer, onNext]);

    return (
        <div className="aha__score d-flex flex-column justify-content-center">
            <div
                className={classNames("score", {
                    zero: score === 0,
                    positive: score > 0,
                    negative: score < 0,
                })}
            >
                <Circle />
                <div className="content">
                    {!icon ? (
                        <div>
                            <h1>
                                {score > 0 && "+"}
                                {showScore}
                            </h1>
                            <h3>{score_message}</h3>
                        </div>
                    ) : (
                        <span className={icon}></span>
                    )}
                </div>
            </div>
            {total_score === 0 ||
                (!!total_score && (
                    <h4 className="total-score">
                        {texts.score}: {total_score - score + showScore}
                    </h4>
                ))}

            {!timer && (
                <div className="d-flex flex-column justify-content-center align-items-center mt-3 mb-4">
                    <Button
                        key={"yes"}
                        className="btn-primary"
                        onClick={onNext}
                        title={texts.next}
                    />
                </div>
            )}

            {last_song && (
                <div className="previous-song">
                    <h4>{texts.listen_explainer}</h4>
                    <p>{last_song}</p>
                </div>
            )}

            {feedback && (
                <p className="feedback text-center">{feedback}</p>
            )}
        </div>
    );
};

export default Score;
