import classNames from "classnames";

interface Rank {
    class: string;
    text: string;
}

interface RankProps {
    rank: Rank;
}

// Rank shows a decorated representation of a rank
const Rank = ({ rank }: RankProps) => {
    return (
        <div
            className={classNames("aha__rank", rank.class, {
                offsetCup: rank.text,
            })}
            data-testid="rank"
        >
            <div className="cup-animation" data-testid="cup-animation" />
            <h4 data-testid="rank-text">{rank.text}</h4>
        </div >
    );
};

export default Rank;
