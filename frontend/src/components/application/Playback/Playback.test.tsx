/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { PlaybackArgs } from "@/types/Playback";
import { describe, expect, it, vi } from "vitest";
import { render } from "@testing-library/react";
import Playback from "./Playback";

vi.mock("@/util/stores");

vi.mock("@/components/application", async (importOriginal) => ({
  ...(await importOriginal<typeof import("@/components/application")>()),
  View: ({ name }) => <div data-testid={`mock-view-${name}`} />,
}));

describe("Playback", () => {
  const basicProps = {
    responseTime: 42,
    onPreloadReady: vi.fn(),
    startedPlaying: vi.fn(),
    finishedPlaying: vi.fn(),
    submitResult: vi.fn(),
  };

  let playbackArgs: PlaybackArgs = {
    view: "BUTTON",
    show_animation: false,
    instruction: "Listen, just listen!",
    play_method: "HTML",
    preload_message: "Get ready",
    sections: [{ id: 13, url: "some/fancy/tune.mp3" }],
    play_from: 0,
  };

  it("renders itself", () => {
    const { container } = render(
      <Playback {...basicProps} playbackArgs={playbackArgs} />
    );
    expect(container.firstChild).toBeTruthy();
  });
});
