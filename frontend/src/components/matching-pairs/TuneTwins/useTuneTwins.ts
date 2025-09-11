/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { Tutorial } from "@/types/tutorial";
import type { Card as CardData } from "@/types/Section";

import { useState, useEffect } from "react";
import classNames from "classnames";
import { scoreIntermediateResult } from "@/API";
import { useTutorial } from "@/hooks/useTutorial";
import { getAudioLatency } from "@/util/time";
import {
  useMatchingPairs,
  CompareCardsProps,
  MPCard,
  MPStates,
  UseMatchingPairsProps,
} from "../MatchingPairs/useMatchingPairs";

export interface TTCard extends MPCard {
  playing?: boolean;
  className?: string;
  data: CardData;
}

export type TTStates = MPStates<TTCard>;

export enum TTGameState {
  DEFAULT = "DEFAULT",
  CARD_SELECTED = "CARD_SELECTED",
  COMPLETED_LUCKY_MATCH = "COMPLETED_LUCKY_MATCH",
  COMPLETED_MEMORY_MATCH = "COMPLETED_MEMORY_MATCH",
  COMPLETED_NO_MATCH = "COMPLETED_NO_MATCH",
  COMPLETED_MISREMEMBERED = "COMPLETED_MISREMEMBERED",
  GAME_END = "GAME_END",
}

export enum TTComparisonResult {
  LUCKY_MATCH = "LUCKY_MATCH",
  MEMORY_MATCH = "MEMORY_MATCH",
  NO_MATCH = "NO_MATCH",
  MISREMEMBERED = "MISREMEMBERED",
}

const DEFAULT_CARD_CLASSES = {
  [TTComparisonResult.NO_MATCH]: "nomatch",
  [TTComparisonResult.LUCKY_MATCH]: "lucky",
  [TTComparisonResult.MISREMEMBERED]: "misremembered",
  [TTComparisonResult.MEMORY_MATCH]: "memory",
};

/**
 * Function that compares two cards and returns the result of the comparison.
 * In this case, it sends a request to the server to get the score. The result
 * of the comparison is determined based on the score returned by the server.
 */
const DEFAULT_COMPARE_CARDS = async (
  card1: TTCard,
  card2: TTCard,
  { startOfTurn, participant, session }: CompareCardsProps<TTCard>
): Promise<[TTComparisonResult, number] | void> => {
  // TODO or should the latency be set immediately when the first card is turned?
  const latency = getAudioLatency();
  const response = await scoreIntermediateResult({
    session,
    participant,
    result: {
      start_of_turn: startOfTurn,
      first_card: {
        ...card1.data,
        seen: card1.hasBeenSelected,
        audio_latency_ms: latency,
      },
      second_card: {
        ...card2.data,
        seen: card2.hasBeenSelected,
        audio_latency_ms: latency,
      },
      // What was this used for?
      overlay_was_shown: false,
    },
  });
  if (!response) throw new Error();
  switch (response.score) {
    case 20:
      return [TTComparisonResult.MEMORY_MATCH, response.score];
    case 10:
      return [TTComparisonResult.LUCKY_MATCH, response.score];
    case 0:
      return [TTComparisonResult.NO_MATCH, response.score];
    case -10:
      return [TTComparisonResult.MISREMEMBERED, response.score];
    default:
      return;
  }
};

// Type of the hook used for typing callbacks like afterSelectPair
type UseMPProps = UseMatchingPairsProps<TTComparisonResult, TTCard>;

export interface UseTuneTwinsProps {
  /** Cards to be used in the game */
  cards: TTCard[];

  /** Animate the card based on the comparison result */
  animate?: boolean;

  /** Callback called when a card is selected */
  onSelectCard?: (card: TTCard) => void;

  /** Callback called when a turn ends */
  onTurnEnd?: (states: TTStates) => void;

  /** Callback called when the game ends */
  onGameEnd?: (states: TTStates) => void;

  /**
   * If set, after selecting two cards, the board is automatically reset
   * after this number of seconds. Defaults to 10 seconds.
   */
  endTurnAfterInterval?: number;

  /** Tutorial object */
  tutorial?: Tutorial;

  /**
   * ClassNames to apply to the cards depending on the comparison result
   */
  cardClasses?: Record<TTComparisonResult, string>;

  /**
   * Feedback messages depending on the game state. For every game state
   * you can pass a list of feedback messages. One will be picked at random
   * from the list.
   */
  feedbackMessages?: Record<TTGameState, string[]>;

  // Only here for testing purposes; shouldn't be changed.
  _compareCards?: CompareCardsProps<TTCard>;
}

export function useTuneTwins({
  cards: initialCards,
  onSelectCard = () => {},
  onTurnEnd: onTurnEndCallback = () => {},
  onGameEnd: onGameEndCallback = () => {},
  endTurnAfterInterval = 10,
  animate = true,
  cardClasses = DEFAULT_CARD_CLASSES,
  feedbackMessages,
  tutorial,
  _compareCards = DEFAULT_COMPARE_CARDS,
}: UseTuneTwinsProps) {
  // Game state that flags UI changes
  const [gameState, setTTGameState] = useState<TTGameState>(
    TTGameState.DEFAULT
  );

  // Tutorial
  const { showStep, completeStep, getActiveSteps } = useTutorial({
    tutorial,
  });

  const beforeSelectCard: UseMPProps["beforeSelectCard"] = ({ card }) => {
    setTTGameState(TTGameState.CARD_SELECTED);
    onSelectCard(card);
  };

  const afterSelectFirstCard: UseMPProps["afterSelectFirstCard"] = ({
    card,
  }) => {
    setTTGameState(TTGameState.CARD_SELECTED);
    return (prev: TTCard[]) =>
      prev.map((c) => (c.id === card.id ? { ...c, playing: true } : { ...c }));
  };

  const afterSelectPair: UseMPProps["afterSelectPair"] = ({
    result,
    card1,
    card2,
  }) => {
    setTTGameState(TTGameState[`COMPLETED_${result}`]);

    // Show tutorial
    if (tutorial) showStep(result.toLocaleLowerCase());
    return (prev: TTCard[]) =>
      prev.map((c) => {
        if (c.id === card1.id)
          return {
            ...c,
            playing: undefined,
            className: classNames(animate && cardClasses[result]),
          };
        if (c.id === card2.id)
          return {
            ...c,
            playing: true,
            className: classNames(animate && cardClasses[result]),
          };
        return { ...c };
      });
  };

  const onTurnEnd: UseMPProps["onTurnEnd"] = (states) => {
    setTTGameState(TTGameState.DEFAULT);
    onTurnEndCallback(states);

    // Finish tutorial step
    if (tutorial) getActiveSteps()?.map((step) => completeStep(step.id));

    // Return cards updater
    return (prev: TTCard[]) =>
      prev.map((c) => ({
        ...c,
        playing: undefined,
        className: undefined,
      }));
  };

  const onGameEnd: UseMPProps["onGameEnd"] = (states: MPStates<TTCard>) => {
    setTTGameState(TTGameState.GAME_END);
    onGameEndCallback(states);
  };

  // Hook up the actual matching pairs game
  const { cards, turnScore, totalScore, endTurn, selectCard } =
    useMatchingPairs<TTComparisonResult, TTCard>({
      cards: initialCards,
      compareCards: _compareCards,
      successfulComparisons: [
        TTComparisonResult.LUCKY_MATCH,
        TTComparisonResult.MEMORY_MATCH,
      ],
      beforeSelectCard,
      afterSelectFirstCard,
      afterSelectPair,
      onTurnEnd,
      onGameEnd,
    });

  // Automatically reset the board after a specified time interval
  useEffect(() => {
    if (!endTurnAfterInterval || !gameState.startsWith("COMPLETED")) return;
    const timeout = setTimeout(endTurn, endTurnAfterInterval * 1000);
    return () => clearTimeout(timeout); // cleanup on unmount or if matched changes
  }, [gameState, endTurn, endTurnAfterInterval]);

  // Feedback meessage
  let feedback;
  if (feedbackMessages) {
    const feedbackContentList = feedbackMessages[gameState] ?? undefined;
    if (feedbackContentList) {
      const randomIdx = Math.floor(Math.random() * feedbackContentList.length);
      feedback = feedbackContentList[randomIdx];
    }
  }

  return {
    showStep,
    completeStep,
    activeSteps: getActiveSteps ? getActiveSteps() : [],
    feedback,
    gameState,
    cards,
    turnScore,
    totalScore,
    endTurn,
    selectCard,
  };
}
