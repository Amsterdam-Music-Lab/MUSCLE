import React from "react";

import Rank from "@/components/Rank/Rank";
import useAnimatedScore from "@/hooks/useAnimatedScore";

interface ScoreProps {
    score: number;
    label: string;
    scoreClass: string; // The rank class, e.g. diamond, platinum, gold, silver, bronze, plastic
}

const Score = ({ score, label, scoreClass }: ScoreProps) => {
    const currentScore = useAnimatedScore(score);

    const rank = {
        class: scoreClass,
        text: "",
    }

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
