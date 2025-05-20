/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { useState } from "react";
import {
  useMatchingPairs,
  MatchingPairsCard,
  UseMatchingPairsProps,
} from "../useMatchingPairs";
import { Board } from "../Board";

interface MPMinimalCard extends MatchingPairsCard {
  data: {
    value: number;
  };
}

enum ComparisonResult {
  MATCH = "MATCH",
  NO_MATCH = "NO_MATCH",
}

enum GameState {
  DEFAULT = "DEFAULT",
  CARD_SELECTED = "CARD_SELECTED",
  MATCH = "COMPLETED_MATCH",
  NO_MATCH = "COMPLETED_NO_MATCH",
  GAME_END = "GAME_END",
}

async function compareCards(
  card1: MPMinimalCard,
  card2: MPMinimalCard
): Promise<[ComparisonResult, number]> {
  if (card1.data.value === card2.data.value) {
    return [ComparisonResult.MATCH, 100];
  } else {
    return [ComparisonResult.NO_MATCH, 0];
  }
}

type UseMPProps = UseMatchingPairsProps<ComparisonResult, MPMinimalCard>;

interface MPMinimalProps {
  cards: MPMinimalCard[];
}

/**
 * A minimal matching pairs game component. The core logic of the game is provided
 * by the useMatchingPairs hook, which handles the game state and card selection.
 * This component renders a very simple board with cards that can be selected,
 * mostly meant for debugging and testing purposes.
 */
export default function MatchingPairsMinimal({
  cards: initialCards,
}: MPMinimalProps) {
  // Game state and updates to it
  const [gameState, setGameState] = useState<GameState>(GameState.DEFAULT);
  const afterSelectFirstCard = () => setGameState(GameState.CARD_SELECTED);
  const afterSelectPair: UseMPProps["afterSelectPair"] = ({ result }) =>
    setGameState(
      result === ComparisonResult.MATCH ? GameState.MATCH : GameState.NO_MATCH
    );
  const onTurnEnd = () => setGameState(GameState.DEFAULT);
  const onGameEnd = () => setGameState(GameState.GAME_END);

  // Set up matching pairs
  const { turnScore, totalScore, cards, endTurn, selectCard } =
    useMatchingPairs<ComparisonResult, MPMinimalCard>({
      cards: initialCards,
      compareCards,
      successfulComparisons: [ComparisonResult.MATCH],
      afterSelectFirstCard,
      afterSelectPair,
      onTurnEnd,
      onGameEnd,
    });

  return (
    <div>
      <div>
        <p>Total score: {totalScore}</p>
        <p>Score: {turnScore ?? "—"}</p>
        <p>State: {gameState}</p>
      </div>
      <Board
        columns={4}
        onClick={() => {
          if ([GameState.MATCH, GameState.NO_MATCH].includes(gameState))
            endTurn();
        }}
      >
        {cards.map((card) => (
          <div
            style={{
              background: card.selected
                ? "lightgreen"
                : card.disabled
                ? "lightgreen"
                : card.hasBeenSelected
                ? "#ccc"
                : "#eee",
              opacity: card.disabled ? 0.15 : 1,
              borderRadius: "1.5em",
              cursor: card.disabled ? "none" : "pointer",
            }}
            className="text-center d-flex flex-column justify-content-center"
            key={card.id}
            onClick={() => {
              selectCard(card.id);
            }}
          >
            <span className="d-block text-muted small">#{card.id}</span>
            <span className="d-block fw-semibold">{card.data.value}</span>
          </div>
        ))}
      </Board>
    </div>
  );
}
