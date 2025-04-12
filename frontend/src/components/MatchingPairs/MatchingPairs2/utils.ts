import { CardData } from "./useMatchingPairs";
import { Tutorial } from "./useTutorial";

/**
 * Utility that creates a proper Tutorial instance from an object mapping
 * matchTypes to the tutorial steps. This should be redundant as soon as
 * the tutorial is handed down properly.
 */
export function processTutorial(tutorial: { [key: string]: string }) {
  const tutorialObj: Tutorial = { steps: [] };
  if (tutorial) {
    Object.keys(tutorial).forEach((matchType) => {
      const step = {
        id: matchType,
        content: tutorial[matchType],
      };
      tutorialObj.steps.push(step);
    });
  }
  return tutorialObj;
}

// TODO this is really not a good solution: if you now set identical
// scores for different match types, you get very unexpected behaviour.
// Instead, the match type name should be passed down from the backend.
export function scoreToMatchType(
  score: number,
  matchTypes: Record<string, { score?: number }>
) {
  if (score === undefined) {
    return matchTypes.default;
  } else {
    for (let name in matchTypes) {
      if (matchTypes[name].score === score) return matchTypes[name];
    }
  }
  throw new Error(
    `Cannot determine match type: score ${score} is not supported.`
  );
}

/**
 * Update all cards with the given updates. Returns copies of the input cards.
 */
export function updateCards(cards: Card[], updates: Partial<Card>): Card[] {
  return cards.map((card) => ({ ...card, ...updates }));
}

/**
 * Update the flipped cards only, leaving other cards untouched. Returns copies
 * of all the cards.
 */
export function updateFlippedCards(
  cards: CardData[],
  updates: Partial<CardData>
): CardData[] {
  return cards.map((card) =>
    card.turned ? { ...card, ...updates } : { ...card }
  );
}
