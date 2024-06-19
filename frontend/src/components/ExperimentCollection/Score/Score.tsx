import React from "react";

import Rank from "@/components/Rank/Rank";
import useAnimatedScore from "@/hooks/useAnimatedScore";

interface ScoreProps {
    score: number;
    label: string;
    scoreClass: string;
}

const Score = ({ score, label, scoreClass }: ScoreProps) => {
    const currentScore = useAnimatedScore(score);

    return (
        <div className="score">
            <Rank rank={{ class: scoreClass }} />
            <h3>
                {currentScore ? currentScore + " " : ""}
                {label}
            </h3>
        </div>
    );
};

export default Score;