/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { http, HttpResponse } from "msw";
import useBoundStore from "@/util/stores";
import { API_BASE_URL } from "@/config";
import { URLS } from "@/API";
import TuneTwins from "./TuneTwins";

import audio from "@/stories/assets/audio.wav";
import { TTCard, TTComparisonResult } from "./useTuneTwins";

const decorator = (Story) => {
  const setSession = useBoundStore((state) => state.setSession);
  const setParticipant = useBoundStore((state) => state.setParticipant);
  setSession({ id: 1 });
  setParticipant({ id: 1, csrf_token: "123" });

  return (
    <div id="root" style={{ width: "100%", height: "100%" }}>
      <Story />
    </div>
  );
};

const meta = {
  title: "Matching Pairs/TuneTwins",
  component: TuneTwins,
  decorators: [decorator],
  tags: ["autodocs"],
};

export default meta;

const cards = Array(16)
  .fill(1)
  .map((_, index) => ({
    id: index,
    data: {
      url: audio,
      group: index % 8,
    },
  }))
  .sort(() => Math.random() - 0.5);

const getMockAPIParams = (response) => ({
  msw: {
    handlers: [
      http.post(API_BASE_URL + URLS.result.intermediateScore, () => {
        return HttpResponse.json(response);
      }),
    ],
  },
});

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

export const Default = {
  args: {
    cards,
    _compareCards: mockComparison(),
  },
};

export const AllMemoryMatch = {
  args: { cards },
  parameters: getMockAPIParams({ score: 20 }),
};

export const MatchLucky = {
  args: {
    cards,
    _compareCards: mockComparison({
      successResult: TTComparisonResult.LUCKY_MATCH,
    }),
  },
};

export const MatchMemory = {
  args: {
    cards,
    _compareCards: mockComparison({
      successResult: TTComparisonResult.LUCKY_MATCH,
    }),
  },
};

export const NoMatchMisremembered = {
  args: {
    cards,
    _compareCards: mockComparison({
      failureResult: TTComparisonResult.MISREMEMBERED,
    }),
  },
};

export const NotAnimated = {
  args: {
    ...Default.args,
    animate: false,
  },
};

const tutorial = {
  steps: [
    {
      id: "no_match",
      content: "The selected cards did not match...",
    },
    {
      id: "memory_match",
      content:
        "The selected cards matched! Very well done, this is absolutely fantastic!",
    },
  ],
  disableCompleted: false,
};

export const Tutorial = {
  args: {
    ...Default.args,
    tutorial,
  },
};

export const Timeline = {
  args: {
    ...Default.args,
    timeline: {
      symbols: ["star-4", "dot", "dot", "star-5", "dot", "dot"],
    },
    timelineStep: 4,
  },
};

export const NoFooter = {
  args: {
    ...Default.args,
    showLogo: false,
    showTimeline: false,
  },
};
