import ScoreCounter, { ScoreCounterProps } from "../ScoreCounter/ScoreCounter";
import Cup, { CupProps } from "../Cup/Cup";

interface RankProps {
    cup: CupProps
    score: ScoreCounterProps;
}

// Rank shows a decorated representation of a rank
const Rank = ({ cup, score }: RankProps) => (
    <div data-testid="rank">
        <Cup className={cup.className} text={cup.text} />
        <ScoreCounter score={score.score} label={score.label} />
    </div>
);

export default Rank;
