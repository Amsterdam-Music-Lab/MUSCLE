/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import Playback from "./Preload";
import audio from "@/assets/audio.wav";

export default {
  title: "Playback/Preload",
  component: Playback,
  parameters: {
    layout: "fullscreen",
  },
};

export const External = {
  args: {
    instruction: "Click the button to play the audio.",
    pageTitle: "Listen to the audio",
    duration: 0,
    sections: [
      {
        id: 1,
        url: audio,
      },
    ],
    playConfig: {
      play_method: "EXTERNAL",
    },
    onNext: () => {},
  },
  decorators: [
    (Story) => (
      <div
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "#ddd",
          padding: "1rem",
        }}
      >
        <Story />
      </div>
    ),
  ],
};
