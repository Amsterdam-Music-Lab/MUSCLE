import { Link } from "react-router-dom";
import { Cup } from "@/components/game";
import { URLS } from "@/config";
import { ParticipantLink } from "@/components/user";

export interface ProfileViewProps {
    messages: {
        title: string;
        summary: string;
        continue: string;
        points: string;
    };
    scores: {
        block_slug: string;
        block_name: string;
        score: number;
        date: string;
        rank: {
            class: string;
            text: string;
        };
        finished_at: string;
    }[];
}

export const ProfileView = (data: ProfileViewProps) => {

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
                                            score.block_slug
                                        )}
                                    >
                                        {score.block_name}
                                    </Link>
                                </h4>
                                <h5>{score.score} {data.messages.points}</h5>
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

export default ProfileView;
