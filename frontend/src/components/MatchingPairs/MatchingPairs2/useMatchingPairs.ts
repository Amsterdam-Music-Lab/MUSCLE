/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { useState } from "react";
import { Card, Card as CardData } from "@/types/Section";
import { updateCards, updateFlippedCards } from "./utils";
import { scoreToMatchType } from "./utils";
import useBoundStore from "@/util/stores";

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

export const MATCH_TYPES = {
  lucky: {
    name: "lucky",
    score: 10,
    gameState: GameState.COMPLETED_LUCKY_MATCH,
  },
  memory: {
    name: "memory",
    score: 20,
    gameState: GameState.COMPLETED_LUCKY_MATCH,
  },
  nomatch: {
    name: "nomatch",
    className: "fbnomatch",
    score: 0,
    gameState: GameState.COMPLETED_NO_MATCH,
  },
  misremembered: {
    name: "misremembered",
    score: -10,
    gameState: GameState.COMPLETED_MISREMEMBERED,
  },
  default: {
    name: "default",
  },
};

interface useMatchingPairsProps {
  initialCards: CardData[];
  initialScore: number;
  compareCards: (
    card1: CardData,
    card2: CardData,
    props: any
  ) => Promise<number | void>;
  onFinishTurn?: () => void;
  onFinishGame?: () => void;
  onMatch?: (any) => void;
}

export function useMatchingPairsLogic({
  initialCards,
  initialScore,
  onFinishTurn = () => {},
  onFinishGame = () => {},
  compareCards = async () => {},
  onMatch = () => {},
}: useMatchingPairsProps) {
  const setError = useBoundStore((s) => s.setError);

  // New state to track card states
  const [cards, setCards] = useState<CardData[]>(() =>
    initialCards.map((card) => ({
      ...card,
      turned: false,
      noevents: false,
      inactive: false,
      seen: false,
      matchClass: "",
    }))
  );

  const [gameState, setGameState] = useState<GameState>(GameState.DEFAULT);
  const [score, setScore] = useState<number | null>(null);
  const [total, setTotal] = useState(initialScore);
  const [startOfTurn, setStartOfTurn] = useState(performance.now());

  const flipCard = async (index: number) => {
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
      setCards((prev) =>
        prev.map((card, i) =>
          i === index ? updatedCard : { ...card, noevents: true }
        )
      );

      // Process the response
      let score;
      try {
        const props = { startOfTurn };
        score = await compareCards(flippedCards[0] as Card, updatedCard, props);
      } catch {
        setError("We cannot currently proceed with the game. Try again later");
        return;
      }

      // Assuming there is no error...
      if (score) {
        const matchType = scoreToMatchType(score, MATCH_TYPES);
        setScore(score);
        setTotal(total + score);
        setGameState(matchType.gameState);
        onMatch(matchType);

        // Add a feedback class to the flipped cards
        setCards((prev) =>
          updateFlippedCards(prev, {
            matchClass: matchType.className,
            seen: true,
          })
        );
      }
    }
  };

  const finishTurn = () => {
    onFinishTurn();
    setStartOfTurn(performance.now());

    // Inactivate the flipped cards if there was a match
    let updatedCards = cards as CardData[];
    if (score === 10 || score === 20) {
      updatedCards = updateFlippedCards(updatedCards, { inactive: true });
    }

    // Reset all cards
    const updates = { turned: false, noevents: false, matchClass: "" };
    updatedCards = updateCards(updatedCards, updates);

    // Update states
    setCards(updatedCards);

    // Check if the board is empty
    if (updatedCards.filter((s) => s.inactive).length === cards.length) {
      setGameState(GameState.BOARD_COMPLETED);
      onFinishGame();
    } else {
      setScore(null);
      setGameState(GameState.DEFAULT);
    }
  };

  return {
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
    finishTurn,
    flipCard,
  };
}
