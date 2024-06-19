import Rank from "@/components/Rank/Rank";
import useAnimatedScore from "@/hooks/useAnimatedScore";

const Score = ({ score, label, scoreClass }) => {
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