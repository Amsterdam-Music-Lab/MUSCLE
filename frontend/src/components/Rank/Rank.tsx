import classNames from "classnames";

export interface RankPayload {
    class: string | "diamond" | "platinum" | "gold" | "silver" | "bronze" | "plastic";
    text: string;
}

interface RankProps {
    rank: RankPayload;
}

// Rank shows a decorated representation of a rank
const Rank = ({ rank }: RankProps) => (
    <div
        className={classNames("aha__rank", rank.class, {
            offsetCup: rank.text,
        })}
        data-testid="rank"
    >
        <div className="cup" data-testid="cup-animation" />
        <h4 data-testid="rank-text">{rank.text}</h4>
    </div >
);

export default Rank;
