/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type Participant from "@/types/Participant";
import { type Session } from "@sentry/react";

import { useState } from "react";
import useBoundStore from "@/util/stores";
import { applyCardUpdates } from "./utils";

export interface MPCard {
  id: number;
  selected?: boolean;
  disabled?: boolean;
  hasBeenSelected?: boolean;
  lastSelectedAt?: number;
  data?: any;
}

export interface MPStates<Card> {
  /** The cards */
  cards: Card[];

  /** The score in the current turn */
  turnScore: number | null;

  /** The total score */
  totalScore: number;
  successfulMatch: boolean | null;
  startOfTurn: number;
}

export interface CompareCardsProps<Card> extends MPStates<Card> {
  /** Participant object */
  participant: Participant | null;

  /** Session object */
  session: Session | null;
}

export type CardUpdater<Card> = (prev: Card[]) => Card[];

export interface UseMatchingPairsProps<ComparisonResult, Card> {
  /** The list of cards */
  cards: Card[];

  /** A function that compares two cards and returns a turnScore */
  compareCards: (
    card1: Card,
    card2: Card,
    props: CompareCardsProps<Card>
  ) => Promise<[ComparisonResult, number] | void>;

  /** A list of comparison results that are considered a match. */
  successfulComparisons: ComparisonResult[];

  /**
   * The initial score the game starts with. This will default to the
   * bonus points, if the block has set any, or zero otherwise.
   */
  initialScore?: number;

  /**
   * Hook called after selecting the first card.
   */
  afterSelectFirstCard?: (
    props: { card: Card } & MPStates<Card>
  ) => CardUpdater<Card> | void;

  /**
   * Hook called before selecting a pair of cards. The properties object contains
   * card1 and card 2 (in the order they were selected), and all states and state
   * setters for the game.
   */
  beforeSelectPair?: (
    props: {
      card1: Card;
      card2: Card;
    } & MPStates<Card>
  ) => CardUpdater<Card> | void;

  /**
   * Hook called after selecting a pair of cards and completing the comparison.
   * The properties object contains card1 and card 2 (in the order they were selected),
   * and all states and state setters for the game.
   */
  afterSelectPair?: (
    props: {
      card1: Card;
      card2: Card;
      result: ComparisonResult;
    } & MPStates<Card>
  ) => CardUpdater<Card> | void;

  /**
   * Hook called on finishing a turn. An object with all states and state setters
   * is passed to the hook.
   */
  onTurnEnd?: (states: MPStates<Card>) => CardUpdater<Card> | void;

  /**
   * Hook called on finishing the entire game.
   * An object with all states and state setters is passed to the hook.
   */
  onGameEnd?: (states: MPStates<Card>) => void;
}

export function useMatchingPairs<ComparisonResult, Card extends MPCard>({
  cards: initialCards,
  successfulComparisons,
  initialScore,
  compareCards = async () => {},
  afterSelectFirstCard = () => {},
  beforeSelectPair = () => {},
  afterSelectPair = () => {},
  onTurnEnd = () => {},
  onGameEnd = () => {},
}: UseMatchingPairsProps<ComparisonResult, Card>) {
  // Variables bound to global store
  const block = useBoundStore((s) => s.block);
  const participant = useBoundStore((s) => s.participant);
  const session = useBoundStore((s) => s.session);
  const setError = useBoundStore((s) => s.setError);

  // Use bonus points if set as default initialScore, unless something
  // else is provided.
  initialScore = initialScore ?? block?.bonus_points ?? 0;

  // New state to track card states
  const [cards, setCards] = useState<Card[]>(() =>
    initialCards.map((card) => ({
      ...card,
      selected: false,
      disabled: false,
      hasBeenSelected: false,
    }))
  );
  const [turnScore, setTurnScore] = useState<number | null>(null);
  const [totalScore, setTotalScore] = useState<number>(initialScore);
  const [successfulMatch, setSuccessfulMatch] = useState<boolean | null>(false);
  const [startOfTurn, setStartOfTurn] = useState<number>(performance.now());

  // Object with all states. This is passed around to all hooks
  const allStates: MPStates<Card> = {
    cards,
    turnScore,
    totalScore,
    successfulMatch,
    startOfTurn,
  };

  /**
   * Function that selects the card with the given index.
   */
  const selectCard = async (id: number) => {
    const card = cards.filter((c) => c.id === id)[0];
    // TODO remove dependency on index; only use id!
    const index = cards.findIndex((c) => c.id === id);
    const selected = cards.filter((s) => s.selected);

    // You cannot select a disabled card, nor an already selected card.
    if (card.disabled) return;
    if (selected.length === 1 && selected[0].id === card.id) return;

    const updatedCard = {
      ...card,
      selected: true,
      hasBeenSelected: true,
      lastSelectedAt: performance.now(),
    };

    // No cards have been flipped; this is the first card
    if (selected.length === 0) {
      const updater = afterSelectFirstCard({ card, ...allStates });
      setCards(
        applyCardUpdates(
          // Note that the order of the updates matters, since updatedCard
          // has already been defined above
          (prev) => prev.map((card, i) => (i === index ? updatedCard : card)),
          typeof updater === "function" ? updater : undefined
        )
      );
    }

    // One card has been flipped, this is the second
    else if (selected.length === 1) {
      const [card1, card2] = [selected[0], updatedCard];

      // Call hook and allow it to update cards
      const updaterBefore = beforeSelectPair({ card1, card2, ...allStates });
      setCards(
        applyCardUpdates(
          (prev) => prev.map((card, i) => (i === index ? updatedCard : card)),
          typeof updaterBefore === "function" ? updaterBefore : undefined
        )
      );

      // Process the response
      let result, resultScore;
      try {
        const props: CompareCardsProps<Card> = {
          participant,
          session,
          ...allStates,
        };
        const outcome = await compareCards(card1, card2, props);
        if (!outcome) throw new Error();
        [result, resultScore] = outcome;
      } catch {
        setError("We cannot currently proceed with the game. Try again later");
        return;
      }

      // Update all states
      setTurnScore(resultScore);
      setTotalScore(totalScore + resultScore);
      setSuccessfulMatch(successfulComparisons.includes(result));

      // Call hook and allow it to update cards
      const updaterAfter = afterSelectPair({
        card1,
        card2,
        result,
        ...allStates,
      });
      if (typeof updaterAfter === "function") setCards(updaterAfter);
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
    setStartOfTurn(performance.now());

    // Let onTurnEnd update the cards if needed
    const updater = onTurnEnd(allStates);

    // Update states
    setCards(
      applyCardUpdates(
        typeof updater === "function" ? updater : undefined,
        (prev) => {
          // Inactivate flipped cards if there was a match, and deselect all cards
          return prev.map((card) => {
            if (card.selected && successfulMatch) {
              return { ...card, selected: false, disabled: true };
            }
            return { ...card, selected: false };
          });
        }
      )
    );
    setSuccessfulMatch(null);

    // Check if the board is empty. Note that cards are not yet updated,
    // so if the match was successful two cards have not yet been counted.
    let numDisabled = cards.filter((s) => s.disabled).length;
    if (successfulMatch) numDisabled += 2;
    if (numDisabled === cards.length) {
      onGameEnd(allStates);
    } else {
      setTurnScore(null);
    }
  };

  return { ...allStates, setCards, endTurn, selectCard };
}
