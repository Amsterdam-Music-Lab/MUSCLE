import { CreateCardProps } from "../createCard";
import { type Card as CardData } from "@/types/Section";
import PlayingBoard from "../PlayingBoard";
import PlayCard from "../PlayCard";

interface MatchingPairsBoardProps 
  extends Omit<CreateCardProps, "playing" | "key", "onClick"> 
  {
    cards: CardData[],
    columns: number;
    playerIndex: number;
    checkMatchingPairs: (index: number) => void;
    playSection: (index: number) => void;
  }

function MatchingPairsBoard({
  type, // view
  cards, // sections
  registerUserClicks,
  playerIndex,
  animate, // showAnimation
  columns = 4,
  playSection,
  checkMatchingPairs
}) {
  return (
    <div className="board">
      <PlayingBoard columns={columns}>
        {cards.map((card, index) => (
          <PlayCard
            key={index}
            onClick={() => {
                playSection(index);
                checkMatchingPairs(index);
            }}
            registerUserClicks={registerUserClicks}
            playing={playerIndex === index}
            section={card}
            showAnimation={animate}
            view={type} />
          )
        )}
      </PlayingBoard>
    </div>
  )
}

export default MatchingPairsBoard
