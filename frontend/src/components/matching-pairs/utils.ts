import { type Tutorial } from "@/types/tutorial";

/**
 * Utility that creates a proper Tutorial instance from an object mapping
 * matchTypes to the tutorial steps. This should be redundant as soon as
 * the tutorial is handed down properly.
 */
export function convertTutorial(tutorial: { [key: string]: string }) {
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

/**
 * Utility that applies several updaters to a list of cards.
 */
export function applyCardUpdates<Card>(
  ...updaters: Array<((cards: Card[]) => Card[]) | undefined>
): (prev: Card[]) => Card[] {
  return (prev: Card[]) => {
    return updaters
      .filter((fn): fn is (cards: Card[]) => Card[] => typeof fn === "function")
      .reduce((acc, fn) => fn(acc), prev);
  };
}
