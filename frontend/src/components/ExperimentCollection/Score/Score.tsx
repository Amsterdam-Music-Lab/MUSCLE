import React from "react";

import Rank, { RankPayload } from "@/components/Rank/Rank";
import useAnimatedScore from "@/hooks/useAnimatedScore";

interface ScoreProps {
    score: number;
    label: string;
    rank: RankPayload;
}

const Score = ({ score, label, rank }: ScoreProps) => {
    const currentScore = useAnimatedScore(score);

    return (
        <div className="score">
            <Rank rank={rank} />
            <h3>
                {currentScore ? currentScore + " " : ""}
                {label}
            </h3>
        </div >
    );
};

export default Score;
