import React, { useState, useEffect, useRef } from "react";
import { Link, withRouter } from "react-router-dom";

import Rank from "../Rank/Rank";
import Social from "../Social/Social";

import { URLS } from "@/config";
import { finalizeSession } from "../../API";
import useBoundStore from "../../util/stores";
import ParticipantLink from "../ParticipantLink/ParticipantLink";
import UserFeedback from "../UserFeedback/UserFeedback";

// Final is an experiment view that shows the final scores of the experiment
// It can only be the last view of an experiment
const Final = ({ experiment, participant, score, final_text, action_texts, button,
    onNext, history, show_participant_link, participant_id_only,
    show_profile_link, social, feedback_info, points, rank, logo }) => {
    const [showScore, setShowScore] = useState(0);
    const session = useBoundStore((state) => state.session);

    // Use a ref to prevent doing multiple increments
    // when the render is skipped
    const scoreValue = useRef(0);

    useEffect(() => {
        if (score === 0) {
            return;
        }

        const id = setTimeout(() => {
            // Score step
            const scoreStep = Math.max(
                1,
                Math.min(10, Math.ceil(Math.abs(scoreValue.current - score) / 10))
            );

            // Score are equal, stop
            if (score === scoreValue.current) {
                return;
            }
            // Add / subtract score
            scoreValue.current += Math.sign(score - scoreValue.current) * scoreStep;
            setShowScore(scoreValue.current);
        }, 50);

        return () => {
            clearTimeout(id);
        };
    }, [score, showScore]);

    useEffect(() => {
        finalizeSession({ session, participant });
    }, [session, participant]);

    const isRelativeUrl = (url) => {
        return url && url.startsWith("/");
    }

    return (
        <div className="aha__final d-flex flex-column justify-content-center">
            {rank && (
                <div className="text-center">
                    <Rank rank={rank} />
                    <h1 className="total-score title" data-testid="score">{showScore} {points}</h1>
                </div>
            )}
            <div className="text-center">
                <div dangerouslySetInnerHTML={{ __html: final_text }} />
            </div>
            {button && (
                <div className="text-center pt-4">
                    {!button?.link && (
                        <button data-testid="button" className='btn btn-primary btn-lg' onClick={() => onNext(false)}>
                            {button.text}
                        </button>
                    )}
                    {button?.link && isRelativeUrl(button.link) ? (
                        <Link data-testid="button-link" className='btn btn-primary btn-lg' to={button.link} onClick={() => onNext(false)}>
                            {button.text}
                        </Link>
                    ) : (
                        <a data-testid="button-link" className='btn btn-primary btn-lg' href={button.link} onClick={() => onNext(false)}>
                            {button.text}
                        </a>
                    )}
                </div>
            )}
            {logo && (
                <div className="text-center pt-4">
                    <a href={logo.link}>
                        <img src={logo.image} width="100%" alt="Logo" />
                    </a>
                </div>
            )}
            {social && (<Social
                social={social}
            />
            )}
            {show_profile_link && (
                <div className=" mt-2 d-flex justify-content-center">
                    <a className="home text-center" href={URLS.AMLHome}>
                        {action_texts.all_experiments}
                    </a>
                    <div
                        data-testid="profile-link"
                        className="home text-center"
                        onClick={() => history.push(URLS.profile)}
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
            {feedback_info && (<UserFeedback
                experimentSlug={experiment.slug}
                participant={participant}
                feedbackInfo={feedback_info}
            />)}

        </div>
    );
};

export default withRouter(Final);
