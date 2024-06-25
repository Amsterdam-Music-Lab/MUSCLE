import useAnimatedScore from "@/hooks/useAnimatedScore";

interface ScoreCounterProps {
    score: number;
    label: string;
}

const ScoreCounter = ({ score, label }: ScoreCounterProps) => {
    const currentScore = useAnimatedScore(score);

    return (
        <h3>
            {currentScore || currentScore === 0 ? currentScore + " " : ""}
            {label}
        </h3>
    );
};

export default ScoreCounter;
