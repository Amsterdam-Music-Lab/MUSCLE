import React from "react";
import { Link } from "react-router-dom";
import DefaultPage from "../Page/DefaultPage";
import Loading from "../Loading/Loading";
import Cup from "../Cup/Cup";
import { useParticipantScores } from "../../API";
import { URLS } from "@/config";
import ParticipantLink from "../ParticipantLink/ParticipantLink";

// Profile loads and shows the profile of a participant for a given experiment
const Profile = () => {
    // API hooks
    const [data, loadingData] = useParticipantScores();

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
            view = ProfileView(data);
        }
    }

    // Show profile

    return <DefaultPage className="aha__profile">{view}</DefaultPage>;
};

export const ProfileView = (data) => {

    // Highest score
    data.scores.sort((a, b) =>
        a.finished_at === b.finished_at
            ? 0
            : a.finished_at > b.finished_at
                ? -1
                : 1
    );

    return (
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
                                <Cup className={score.rank.class} text={score.rank.text} />
                            </div>
                            <div className="stats">
                                <h4>
                                    <Link
                                        to={URLS.block.replace(
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
    )
}

export default Profile;
