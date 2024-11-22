import classNames from "classnames";

export interface CupProps {
    className: string | "diamond" | "platinum" | "gold" | "silver" | "bronze" | "plastic";
    text: string;
}


// Rank shows a decorated representation of a rank
const Rank = ({ className, text }: CupProps) => (
    <div
        className={classNames("aha__cup", className, {
            offsetCup: text,
        })}
        data-testid="cup"
    >
        <div className="cup" data-testid="cup-animation" />
        <h4 data-testid="cup-text">{text}</h4>
    </div >
);

export default Rank;
