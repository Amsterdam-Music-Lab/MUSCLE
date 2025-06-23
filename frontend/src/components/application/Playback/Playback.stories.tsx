/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { StoryFn, Meta } from "@storybook/react";
import { useState } from "react";
import { BUTTON } from "@/types/Playback";
import useBoundStore from "@/util/stores";
import { Button } from "@/components/buttons";
import audio from "@/assets/music.ogg";
import Playback from "./Playback";

const meta: Meta<typeof Playback> = {
  title: "App/Controllers/Playback",
  component: Playback,
};
export default meta;

const playbackProps = {
  view: BUTTON,
  show_animation: true,
  preload_message: "Loading audio...",
  instruction: "Click the button to play the audio.",
  sections: [{ id: 0, url: audio }],
  play_from: 0.0,
  resume_play: false,
};

// Create a decorator that dynamically accepts a play_method
const decorator = (play_method: "BUFFER" | "EXTERNAL") => (Story: StoryFn) => {
  const [initialized, setInitialized] = useState(false);
  const setCurrentAction = useBoundStore((state) => state.setCurrentAction);
  setCurrentAction({
    view: "TRIAL_VIEW",
    playback: { ...playbackProps, play_method },
  });
  return initialized ? (
    <Story />
  ) : (
    <Button onClick={() => setInitialized(true)}>Initialize</Button>
  );
};

export const AutoplayBuffer = {
  args: {
    playbackArgs: { ...playbackProps, play_method: "BUFFER" },
    responseTime: 5,
    onPreloadReady: () => {},
    submitResult: () => {},
    finishedPlaying: () => {},
  },
  decorators: [decorator("BUFFER")],
};

export const AutoplayExternal = {
  args: {
    ...AutoplayBuffer.args,
    playbackArgs: { ...playbackProps, play_method: "EXTERNAL" },
  },
  decorators: [decorator("EXTERNAL")],
};
