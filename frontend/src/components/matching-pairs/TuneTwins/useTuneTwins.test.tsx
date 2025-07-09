/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { describe, test, expect, vi, afterEach } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { selectCard, playTurn, playCompleteTurn } from "../MatchingPairs/utils";
import {
  useTuneTwins,
  TTGameState,
  TTComparisonResult,
  TTCard,
} from "./useTuneTwins";

const initialState = {
  setError: vi.fn(),
  block: { bonus_points: 0 },
};

vi.mock("@/util/stores", () => ({
  __esModule: true,
  default: (fn: any) => {
    return fn(initialState);
  },
  useBoundStore: vi.fn(),
}));

// Mocks
vi.mock("@/API", () => ({
  scoreIntermediateResult: vi.fn().mockResolvedValue({ score: 10 }),
}));

vi.mock("@/util/time", () => ({
  getAudioLatency: () => 42,
}));

const makeCard = (id: number, data: any = {}) =>
  ({
    id,
    data: { ...data, id },
    selected: false,
    disabled: false,
    hasBeenSelected: false,
  } as TTCard);

const twoCards = [makeCard(1, { group: "A" }), makeCard(2, { group: "A" })];

const fourCards = [
  ...twoCards,
  makeCard(3, { group: "B" }),
  makeCard(4, { group: "B" }),
];

const mockTutorial = {
  steps: [
    {
      id: "no_match",
      content: "content: no_match",
    },
    {
      id: "memory_match",
      content: "content: memory_match",
    },
  ],
};

const defaultFeedback = {
  [TTGameState.DEFAULT]: ["default"],
  [TTGameState.CARD_SELECTED]: ["selected"],
  [TTGameState.COMPLETED_LUCKY_MATCH]: ["lucky"],
  [TTGameState.COMPLETED_MEMORY_MATCH]: ["memory"],
  [TTGameState.COMPLETED_NO_MATCH]: ["no match"],
  [TTGameState.COMPLETED_MISREMEMBERED]: ["misremembered"],
  [TTGameState.GAME_END]: ["end"],
};

// TODO duplicated in TuneTwins.stories.tsx...
interface MockComparisonProps {
  successResult: TTComparisonResult;
  failureResult: TTComparisonResult;
  successScore: number;
  failureScore: numberl;
}

function mockComparison({
  successResult = TTComparisonResult.MEMORY_MATCH,
  failureResult = TTComparisonResult.NO_MATCH,
  successScore = 10,
  failureScore = 0,
}: MockComparisonProps = {}) {
  return async (card1: TTCard, card2: TTCard) => {
    const match = card1.data.group === card2.data.group;
    const result = match ? successResult : failureResult;
    const score = match ? successScore : failureScore;
    return [result, score];
  };
}

const defaultArgs = { cards: twoCards, feedbackMessages: defaultFeedback };

describe("useTuneTwins", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  test("returns initial state and cards", () => {
    const { result } = renderHook(() => useTuneTwins(defaultArgs));
    expect(result.current.cards.length).toBe(2);
    expect(result.current.gameState).toBe(TTGameState.DEFAULT);
    expect(result.current.feedback).toBe("default");
  });

  test("calls onSelectCard and updates gameState on card select", async () => {
    const onSelectCard = vi.fn();
    const { result } = renderHook(() =>
      useTuneTwins({ ...defaultArgs, onSelectCard })
    );
    await selectCard(result, 1);
    expect(onSelectCard).toHaveBeenCalled();
    expect(result.current.gameState).toBe(TTGameState.CARD_SELECTED);
    expect(result.current.feedback).toBe("selected");
  });

  test("sets correct gameState and feedback after pair selection", async () => {
    const { result } = renderHook(() => useTuneTwins(defaultArgs));
    await playTurn(result, 1, 2);
    expect([
      TTGameState.COMPLETED_LUCKY_MATCH,
      TTGameState.COMPLETED_MEMORY_MATCH,
    ]).toContain(result.current.gameState);
    expect(["lucky", "memory"]).toContain(result.current.feedback);
  });

  test("calls onTurnEnd and resets state after endTurn", async () => {
    const onTurnEnd = vi.fn();
    const { result } = renderHook(() =>
      useTuneTwins({ ...defaultArgs, cards: fourCards, onTurnEnd })
    );
    await playCompleteTurn(result, 1, 2);
    expect(onTurnEnd).toHaveBeenCalled();
    expect(result.current.gameState).toBe(TTGameState.DEFAULT);
    expect(result.current.feedback).toBe("default");
  });

  test("calls onGameEnd when all pairs matched", async () => {
    const onGameEnd = vi.fn();
    const { result } = renderHook(() =>
      useTuneTwins({ ...defaultArgs, onGameEnd })
    );
    await playCompleteTurn(result, 1, 2);
    expect(onGameEnd).toHaveBeenCalled();
    expect(result.current.gameState).toBe(TTGameState.GAME_END);
    expect(result.current.feedback).toBe("end");
  });

  test("applies cardClasses and animation on afterSelectPair", async () => {
    const { result } = renderHook(() =>
      useTuneTwins({
        ...defaultArgs,
        cardClasses: {
          [TTComparisonResult.LUCKY_MATCH]: "lucky-class",
          [TTComparisonResult.MEMORY_MATCH]: "memory-class",
          [TTComparisonResult.NO_MATCH]: "no-match-class",
          [TTComparisonResult.MISREMEMBERED]: "mis-class",
        },
      })
    );
    await playTurn(result, 1, 2);
    const card = result.current.cards.find((c) => c.id === 2);
    expect(card?.className).toMatch(/lucky-class|memory-class/);
  });

  test("auto ends turn after interval", async () => {
    vi.useFakeTimers();
    const { result } = renderHook(() =>
      useTuneTwins({
        ...defaultArgs,
        endTurnAfterInterval: 2,
      })
    );
    await playTurn(result, 1, 2);
    expect(result.current.gameState).not.toBe(TTGameState.DEFAULT);
    await act(async () => vi.advanceTimersByTime(1000));
    expect(result.current.gameState).not.toBe(TTGameState.GAME_END);
    await act(async () => vi.advanceTimersByTime(1000));
    expect(result.current.gameState).toBe(TTGameState.GAME_END);
    vi.useRealTimers();
  });

  test("tutorial step is activated and getActiveSteps returns it", async () => {
    const { result } = renderHook(() =>
      useTuneTwins({
        ...defaultArgs,
        _compareCards: mockComparison(),
        tutorial: mockTutorial,
      })
    );
    await playTurn(result, 1, 2);
    expect(result.current.activeSteps.length).toBe(1);
    expect(result.current.activeSteps[0].id).toBe("memory_match");
  });
});
