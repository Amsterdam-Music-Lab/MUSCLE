import React, { useRef } from "react";
import { Link } from "react-router-dom";
import DefaultPage from "../Page/DefaultPage";
import Loading from "../Loading/Loading";
import Rank from "../Rank/Rank";
import { useParticipantScores, useParticipantLink } from "../../API";
import { URLS } from "../../config";
import ParticipantLink from "../ParticipantLink/ParticipantLink";

// Profile loads and shows the profile of a participant for a given experiment
const Profile = () => {
    // API hooks
    const [data, loadingData] = useParticipantScores();
    const linkInput = useRef();

    const copyLink = () => {
        if (!linkInput.current) {
            return;
        }

        // Select text
        linkInput.current.select();

        // For mobile
        linkInput.current.setSelectionRange(0, 99999);

        // Copy
        document.execCommand("copy");
    };

    // View
    let view = null;
    switch (true) {
        case loadingData:
            view = <Loading />;
            break;
        case data === null:
            view = (
                <Loading>
                    An error occurred while
                    <br />
                    loading your profile
                </Loading>
            );
            break;
        default: {
            // Highest score
            data.scores.sort((a, b) =>
                a.finished_at === b.finished_at
                    ? 0
                    : a.finished_at > b.finished_at
                    ? -1
                    : 1
            );
            view = (
                <>
                    <h3 className="title">{data.messages.title}</h3>
                    <p>
                        {data.messages.summary}
                    </p>

                    <div className="scroller">
                        <div
                            className="scores"
                            style={{ width: 25 + data.scores.length * 290 }}
                        >
                            {data.scores.map((score, index) => (
                                <div key={index} className="score">
                                    <div className="rank">
                                        <Rank rank={score.rank} />
                                    </div>
                                    <div className="stats">
                                        <h4>
                                            <Link
                                                to={URLS.experiment.replace(
                                                    ":slug",
                                                    score.experiment_slug
                                                )}
                                            >
                                                {score.experiment_name}
                                            </Link>
                                        </h4>
                                        <h5>{score.score} {data.points}</h5>
                                        <p>{score.date}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="store">
                        <p>
                            {data.messages.continue}
                        </p>
                        <ParticipantLink></ParticipantLink>
                    </div>
                </>
            );
        }
    }

    // Show profile

    return <DefaultPage className="aha__profile">{view}</DefaultPage>;
};

export default Profile;
