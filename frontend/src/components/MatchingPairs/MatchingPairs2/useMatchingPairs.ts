/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { useState } from "react";
import { Session } from "@sentry/react";
import { Card } from "@/types/Section";
import Participant from "@/types/Participant";
import useBoundStore from "@/util/stores";
import { updateCards, updateFlippedCards } from "./utils";

// TODO rename turned ==> selected

export interface CardData extends Card {
  comparisonResult?: ComparisonResult;
}

export enum GameState {
  DEFAULT = "DEFAULT",
  FIRST_CARD_SELECTED = "FIRST_CARD_SELECTED",
  COMPLETED_LUCKY_MATCH = "COMPLETED_LUCKY_MATCH",
  COMPLETED_MEMORY_MATCH = "COMPLETED_MEMORY_MATCH",
  COMPLETED_NO_MATCH = "COMPLETED_NO_MATCH",
  COMPLETED_MISREMEMBERED = "COMPLETED_MISREMEMBERED",
  BOARD_COMPLETED = "BOARD_COMPLETED",
}

/** Tests whether the game state corresponds to one where a turn is just completed */
export const isTurnComplete = (gameState: GameState) =>
  gameState === GameState.COMPLETED_LUCKY_MATCH ||
  gameState === GameState.COMPLETED_MEMORY_MATCH ||
  gameState === GameState.COMPLETED_NO_MATCH ||
  gameState === GameState.COMPLETED_MISREMEMBERED;

export interface MatchingPairsStates {
  gameState: GameState;
  setGameState: React.Dispatch<React.SetStateAction<GameState>>;
  cards: CardData[];
  setCards: React.Dispatch<React.SetStateAction<CardData[]>>;
  score: number | null;
  setScore: React.Dispatch<React.SetStateAction<number | null>>;
  total: number;
  setTotal: React.Dispatch<React.SetStateAction<number>>;
  startOfTurn: number;
  setStartOfTurn: React.Dispatch<React.SetStateAction<number>>;
}

/**
 * The possible outcomes of a comparison between two cards.
 */
export enum ComparisonResult {
  LUCKY_MATCH = "LUCKY_MATCH",
  MEMORY_MATCH = "MEMORY_MATCH",
  NO_MATCH = "NO_MATCH",
  MISREMEMBERED = "MISREMEMBERED",
}

export interface CompareCardsProps extends MatchingPairsStates {
  /** Participant object */
  participant: Participant | null;

  /** Session object */
  session: Session | null;
}

interface useMatchingPairsProps {
  /** The list of cards */
  cards: CardData[];

  /** A function that compares two cards and returns a score */
  compareCards: (
    card1: CardData,
    card2: CardData,
    props: CompareCardsProps
  ) => Promise<[ComparisonResult, number] | void>;

  /**
   * The initial score the game starts with. This will default to the
   * bonus points, if the block has set any, or zero otherwise.
   */
  initialScore?: number;

  /**
   * Hook called before selecting a pair of cards. The first two arguments are
   * the two cards (in the order they were selected), the second argument is an
   * object with all states and state setters for the game.
   */
  beforeSelectPair?: (
    card1: CardData,
    card2: CardData,
    states: MatchingPairsStates
  ) => void;

  /**
   * Hook called after selecting a pair of cards and completing the comparison.
   * The first argument will be the result of the comparison, the second an
   * object with all states and state setters for the game.
   */
  afterSelectPair?: (
    result: ComparisonResult,
    states: MatchingPairsStates
  ) => void;

  /**
   * Hook called on finishing a turn. An object with all states and state setters
   * is passed to the hook.
   */
  onTurnEnd?: (states: MatchingPairsStates) => void;

  /**
   * Hook called on finishing the entire game.
   * An object with all states and state setters is passed to the hook.
   */
  onGameEnd?: (states: MatchingPairsStates) => void;
}

export function useMatchingPairs({
  cards: initialCards,
  initialScore,
  compareCards = async () => {},
  beforeSelectPair = () => {},
  afterSelectPair = () => {},
  onTurnEnd = () => {},
  onGameEnd = () => {},
}: useMatchingPairsProps) {
  // Variables bound to global store
  const block = useBoundStore((s) => s.block);
  const participant = useBoundStore((s) => s.participant);
  const session = useBoundStore((s) => s.session);
  const setError = useBoundStore((s) => s.setError);

  // Use bonus points if set as default initialScore, unless something
  // else is provided.
  initialScore = initialScore ?? block?.bonus_points ?? 0;

  // New state to track card states
  const [cards, setCards] = useState<CardData[]>(() =>
    initialCards.map((card) => ({
      ...card,
      turned: false,
      noevents: false,
      inactive: false,
      seen: false,
    }))
  );
  const [gameState, setGameState] = useState<GameState>(GameState.DEFAULT);
  const [score, setScore] = useState<number | null>(null);
  const [total, setTotal] = useState<number>(initialScore);
  const [startOfTurn, setStartOfTurn] = useState<number>(performance.now());

  // Object with all states. This is passed around to all hooks
  const allStates: MatchingPairsStates = {
    gameState,
    setGameState,
    cards,
    setCards,
    score,
    setScore,
    total,
    setTotal,
    startOfTurn,
    setStartOfTurn,
  };

  /**
   * Function that selects the card with the given index.
   */
  const selectCard = async (index: number) => {
    const flippedCards = cards.filter((s) => s.turned);
    const card = cards[index];
    const updatedCard = {
      ...card,
      turned: true,
      noevents: true,
      boardposition: index + 1,
      timestamp: performance.now(),
    };

    // No cards have been flipped; this is the first card
    if (flippedCards.length === 0) {
      setCards((prev) =>
        prev.map((card, i) => (i === index ? updatedCard : card))
      );
      setGameState(GameState.FIRST_CARD_SELECTED);
    }

    // One card has been flipped, this is the second
    else if (flippedCards.length === 1) {
      const [card1, card2] = [flippedCards[0], updatedCard];
      beforeSelectPair(card1, card2, allStates);

      setCards((prev) =>
        prev.map((card, i) =>
          i === index ? updatedCard : { ...card, noevents: true }
        )
      );

      // Process the response
      let result, resultScore;
      try {
        const props: CompareCardsProps = { participant, session, ...allStates };
        const outcome = await compareCards(card1, card2, props);
        if (!outcome) throw new Error();
        [result, resultScore] = outcome;
      } catch {
        setError("We cannot currently proceed with the game. Try again later");
        return;
      }

      // Update all states
      setScore(resultScore);
      setTotal(total + resultScore);
      const updates = { seen: true, comparisonResult: result };
      setCards((prev) => updateFlippedCards(prev, updates));
      setGameState(GameState[`COMPLETED_${result}`]);

      // Call hook
      afterSelectPair(result, allStates);
    }
  };

  /**
   * Function that ends the current turn, and prepares the board
   * for the next turn. If all cards have been removed from the board,
   * the game ends and onGameEnd is called.
   *
   * Note that the function is only executed if the current turn has
   * indeed been completed.
   */
  const endTurn = () => {
    if (!isTurnComplete(gameState)) return;
    setStartOfTurn(performance.now());
    onTurnEnd(allStates);

    // Inactivate the flipped cards if there was a match
    let updatedCards = cards as CardData[];
    if (score === 10 || score === 20) {
      updatedCards = updateFlippedCards(updatedCards, { inactive: true });
    }

    // Reset all cards
    const updates = { turned: false, noevents: false, comparisonResult: null };
    updatedCards = updateCards(updatedCards, updates);

    // Update states
    setCards(updatedCards);

    // Check if the board is empty
    if (updatedCards.filter((s) => s.inactive).length === cards.length) {
      setGameState(GameState.BOARD_COMPLETED);
      onGameEnd(allStates);
    } else {
      setScore(null);
      setGameState(GameState.DEFAULT);
    }
  };

  return { ...allStates, endTurn, selectCard };
}
