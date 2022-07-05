import React, { useState, useEffect, useRef } from "react";
import { withRouter } from "react-router-dom";

import Rank from "../Rank/Rank";
import Social from "../Social/Social";

import { URLS } from "../../config";
import ParticipantLink from "../ParticipantLink/ParticipantLink";

// Final is an experiment view that shows the final scores of the experiment
// It can only be the last view of an experiment
const Final= ({ score, final_text, action_texts, button, onNext, history, show_participant_link, participant_id_only, show_profile_link, show_social, points, rank }) => {
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
            {rank && (
            <div className="text-center">
                <Rank rank={rank} />
                <h1 className="total-score title">{showScore} {points}</h1>
            </div>
            )}
            <div>
                <div dangerouslySetInnerHTML={{ __html: final_text }} />
            </div>
            {button && (
                <a className="text-center" href={button.link}>
                    <button className='btn btn-primary btn-lg'>
                        {button.text}
                    </button>
                </a>
            )}
            {show_social && (<Social
                score={score}
            />
            )}
            {show_profile_link && (
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
            )}
            {show_participant_link && (
                <ParticipantLink
                    participantIDOnly={participant_id_only}
                />
            )}
        </div>
    );
};

export default withRouter(Final);
