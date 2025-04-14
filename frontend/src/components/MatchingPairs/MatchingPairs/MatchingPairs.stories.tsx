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
import MatchingPairs from "./MatchingPairs";

import audio from "@/stories/assets/audio.wav";
import catImage from "@/stories/assets/images/cat-01.webp";

const decorator = (Story) => {
  const setSession = useBoundStore((state) => state.setSession);
  const setParticipant = useBoundStore((state) => state.setParticipant);
  setSession({ id: 1 });
  setParticipant({ id: 1, csrf_token: "123" });

  return (
    <div id="root" style={{ width: "100%", height: "100%", padding: "1rem" }}>
      <Story />
    </div>
  );
};

export default {
  title: "Matching Pairs/Matching Pairs",
  component: MatchingPairs,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

const audioCards = Array(16)
  .fill(1)
  .map((_, index) => ({
    id: index,
    data: {
      url: audio,
      group: index % 8,
    },
  }))
  .sort(() => Math.random() - 0.5);

const visualCards = Array(16)
  .fill(1)
  .map((_, index) => ({
    id: index,
    data: {
      src: `http://localhost:6006${catImage}`,
      alt: "Image of a cat",
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

export const AllMemoryMatch = {
  args: {
    cards: audioCards,
    type: "audio",
  },
  decorators: [decorator],
  parameters: getMockAPIParams({ score: 20 }),
};

export const AllLuckyMatch = {
  args: {
    cards: audioCards,
    type: "audio",
  },
  decorators: [decorator],
  parameters: getMockAPIParams({ score: 10 }),
};

export const AllNoMatch = {
  args: {
    cards: audioCards,
    type: "audio",
  },
  decorators: [decorator],
  parameters: getMockAPIParams({ score: 0 }),
};

export const AllMisremembered = {
  args: {
    cards: audioCards,
    type: "audio",
  },
  decorators: [decorator],
  parameters: getMockAPIParams({ score: -10 }),
};

export const AllLuckyNotAnimated = {
  args: {
    cards: audioCards,
    type: "audio",
    animate: false,
  },
  decorators: [decorator],
  parameters: getMockAPIParams({ score: -10 }),
};

export const Visual = {
  args: {
    cards: visualCards,
    type: "visual",
  },
  decorators: [decorator],
  parameters: getMockAPIParams({ score: 10 }),
};
