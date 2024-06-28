import useAnimatedScore from "@/hooks/useAnimatedScore";

export interface ScoreCounterProps {
    score: number;
    label: string;
}

const ScoreCounter = ({ score, label }: ScoreCounterProps) => {
    const currentScore = useAnimatedScore(score);

    return (
        <h3 data-testid="score">
            {currentScore || currentScore === 0 ? currentScore + " " : ""}
            {label}
        </h3>
    );
};

export default ScoreCounter;
