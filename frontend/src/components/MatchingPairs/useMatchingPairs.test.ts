/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { MPCard, UseMatchingPairsProps } from "./useMatchingPairs";

import { vi, describe, expect, test, afterEach } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useMatchingPairs } from "./useMatchingPairs";

const initialState = {
  // participant: 1,
  // session: 1,
  // setError: vi.fn(),
  block: { bonus_points: 0 },
  // currentAction: () => ({ view: "TRIAL_VIEW" }),
};

vi.mock("@/util/stores", () => ({
  __esModule: true,
  default: (fn: any) => {
    return fn(initialState);
  },
  useBoundStore: vi.fn(),
}));

interface Card extends MPCard {
  data: string;
}
type ComparisonResult = "match" | "no_match";
type UseMPProps = UseMatchingPairsProps<ComparisonResult, Card>;

const createCards = (): Card[] => [
  { id: 1, data: "A" },
  { id: 2, data: "A" },
  { id: 3, data: "B" },
  { id: 4, data: "B" },
];

const mockCompare: UseMPProps["compareCards"] = async (
  card1: Card,
  card2: Card
) => {
  if (card1.data === card2.data) {
    return ["match" as ComparisonResult, 10];
  } else {
    return ["no_match" as ComparisonResult, 0];
  }
};

const getProps = (props: Partial<UseMPProps> = {}) => ({
  cards: createCards(),
  compareCards: mockCompare,
  successfulComparisons: ["match"],
  ...props,
});

// Helper functions

const filterCards = (result, filter) => result.current.cards.filter(filter);

const selectedCards = (result) => filterCards(result, (c) => c.selected);

const selectCard = async (result, id: number) => {
  await act(async () => {
    await result.current.selectCard(id);
  });
};

const endTurn = async (result) => {
  await act(async () => {
    result.current.endTurn();
  });
};

const playTurn = async (result, id1: number, id2: number) => {
  await selectCard(result, id1);
  await selectCard(result, id2);
};

const playCompleteTurn = async (result, id1: number, id2: number) => {
  await playTurn(result, id1, id2);
  await endTurn(result);
};

// Tests

describe("useMatchingPairs", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.clearAllMocks();
    vi.clearAllTimers();
  });

  test("selects a card as first card", async () => {
    const { result } = renderHook(() =>
      useMatchingPairs<ComparisonResult, Card>(getProps() as UseMPProps)
    );
    await selectCard(result, 1);
    const selected = selectedCards(result);
    expect(selected).toHaveLength(1);
    expect(selected[0].id).toBe(1);
  });

  test("completes a turn with a match", async () => {
    const { result } = renderHook(() =>
      useMatchingPairs<ComparisonResult, Card>(getProps() as UseMPProps)
    );
    await playTurn(result, 1, 2);
    expect(selectedCards(result)).toHaveLength(2);
    expect(result.current.turnScore).toBe(10);

    await endTurn(result);
    const disabled = filterCards(result, (c) => c.disabled);
    expect(disabled.length).toBe(2);
    expect(result.current.totalScore).toBe(10);
  });

  test("completes a turn without a match", async () => {
    const { result } = renderHook(() =>
      useMatchingPairs<ComparisonResult, Card>(getProps() as UseMPProps)
    );
    await playCompleteTurn(result, 1, 3);
    const disabled = result.current.cards.filter((c) => c.disabled);
    expect(disabled.length).toBe(0);
    expect(result.current.totalScore).toBe(0);
  });

  test("selecting the same card twice does not change state", async () => {
    const { result } = renderHook(() =>
      useMatchingPairs<ComparisonResult, Card>(getProps() as UseMPProps)
    );
    await playTurn(result, 1, 1);
    expect(selectedCards(result)).toHaveLength(1);
  });

  test("disabled card cannot be selected", async () => {
    const { result } = renderHook(() =>
      useMatchingPairs<ComparisonResult, Card>(getProps() as UseMPProps)
    );
    await playCompleteTurn(result, 1, 2);
    await selectCard(result, 1);
    expect(selectedCards(result)).toHaveLength(0);
  });

  test("uses initialScore and increases totalScore after match", async () => {
    const { result } = renderHook(() =>
      useMatchingPairs<ComparisonResult, Card>(
        getProps({ initialScore: 200 }) as UseMPProps
      )
    );
    await playCompleteTurn(result, 1, 2);
    expect(result.current.totalScore).toBe(210);
  });

  test("uses block.bonus_points as default initialScore if not provided", () => {
    initialState.block.bonus_points = 100;

    const { result } = renderHook(() =>
      useMatchingPairs({
        cards: [
          { id: 1, data: "X" },
          { id: 2, data: "X" },
        ],
        compareCards: async () => ["match", 10],
        successfulComparisons: ["match"],
      })
    );

    expect(result.current.totalScore).toBe(100);
  });

  test("compareCards is called with correct arguments", async () => {
    const compareCards = vi.fn().mockResolvedValue(["match", 10]);

    const { result } = renderHook(() =>
      useMatchingPairs({
        cards: [
          { id: 1, data: "A" },
          { id: 2, data: "A" },
        ],
        compareCards,
        successfulComparisons: ["match"],
      })
    );

    await playTurn(result, 1, 2);
    expect(compareCards).toHaveBeenCalledTimes(1);
    expect(compareCards).toHaveBeenCalledWith(
      expect.objectContaining({ id: 1 }),
      expect.objectContaining({ id: 2 }),
      expect.any(Object)
    );
  });

  test("afterSelectFirstCard can modify card state", async () => {
    const afterSelectFirstCard =
      ({ card }) =>
      (prev) =>
        prev.map((c) => (c.id === card.id ? { ...c, wasMarked: true } : c));

    const { result } = renderHook(() =>
      useMatchingPairs<ComparisonResult, Card>(
        getProps({ afterSelectFirstCard }) as UseMPProps
      )
    );

    await act(async () => {
      await result.current.selectCard(1);
    });

    expect(result.current.cards[0].wasMarked).toBe(true);
  });

  test("calls onGameEnd when all cards are matched", async () => {
    const onGameEnd = vi.fn();

    const { result } = renderHook(() =>
      useMatchingPairs({
        cards: [
          { id: 1, data: "A" },
          { id: 2, data: "A" },
        ],
        compareCards: async () => ["match", 10],
        successfulComparisons: ["match"],
        onGameEnd,
      })
    );
    await playCompleteTurn(result, 1, 2);
    expect(onGameEnd).toHaveBeenCalled();
  });

  test("Check that onSelectCard is not called for disabled cards", async () => {
    const onSelectCard = vi.fn();

    const { result } = renderHook(() =>
      useMatchingPairs({
        cards: [
          { id: 1, data: "A", disabled: true },
          { id: 2, data: "A", disabled: true },
        ],
        compareCards: async () => ["match", 10],
        successfulComparisons: ["match"],
        beforeSelectCard: ({ card }) => onSelectCard(card),
      })
    );
    await playCompleteTurn(result, 1, 2);
    expect(onSelectCard).not.toHaveBeenCalled();
  });
});
