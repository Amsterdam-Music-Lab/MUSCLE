import {
  useMatchingPairs,
  CardData,
  ComparisonResult,
  CompareCardsProps,
} from "./useMatchingPairs";

import { Board } from "../Board";

interface MinimalMatchingPairsProps {
  cards: CardData[];
}

async function compareCards(
  card1: CardData,
  card2: CardData,
  props: CompareCardsProps
): Promise<[ComparisonResult, number]> {
  if (card1.value == card2.value) {
    return [ComparisonResult.LUCKY_MATCH, 10];
  } else {
    return [ComparisonResult.NO_MATCH, 0];
  }
}

export default function MinimalMatchingPairs({
  cards: initialCards,
}: MinimalMatchingPairsProps) {
  const { gameState, cards, endTurn, selectCard } = useMatchingPairs({
    cards: initialCards,
    compareCards,
  });
  console.log(cards);

  return (
    <Board columns={4} onClick={endTurn}>
      {cards.map((card, index) => (
        <div
          style={{
            background: card.turned ? "yellow" : "#eee",
            opacity: card.inactive ? 0.3 : 1,
            borderRadius: "1.5em",
          }}
          className="text-center d-flex flex-column justify-content-center"
          key={card.id}
          onClick={() => {
            selectCard(index);
          }}
        >
          <span className="d-block text-muted small">#{card.id}</span>
          <span className="d-block fw-semibold">{card.value}</span>
        </div>
      ))}
    </Board>
  );
}
