/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import Trial from "./Trial";

export default {
  title: "App/Controllers/Trial",
  component: Trial,
};

const question1 = {
  key: "know_song",
  view: "BUTTON_ARRAY",
  explainer: "",
  question: "1. Do you know this song?",
  is_skippable: false,
  submits: false,
  style: { boolean: true },
  choices: {
    yes: "fa-check",
    unsure: "fa-question",
    no: "fa-xmark",
  },
  min_values: 1,
};

const question2 = {
  key: "like_song",
  view: "ICON_RANGE",
  explainer: "",
  question: "2. How much do you like this song?",
  is_skippable: false,
  submits: false,
  style: { "gradient-7": true },
  choices: {
    1: "fa-face-grin-hearts",
    2: "fa-face-grin",
    3: "fa-face-smile",
    4: "fa-face-meh",
    5: "fa-face-frown",
    6: "fa-face-frown-open",
    7: "fa-face-angry",
  },
};

const feedbackForm = {
  form: [question1, question2],
  submit_label: "Submit",
  skip_label: "Skip",
  is_skippable: true,
  is_profile: true,
};

const sections = [
  {
    start: 0,
    end: 10,
    text: "This is the first section",
  },
  {
    start: 10,
    end: 20,
    text: "This is the second section",
  },
];

const playbackArgs = {
  play_method: "NOAUDIO",
  view: "BUTTON",
  instruction: "This is the instruction",
  preload_message: "This is the preload message",
  play_config: {
    autoplay: true,
    controls: true,
    loop: true,
    muted: true,
    playback_rate: 1,
    preload: "auto",
  },
  sections,
};

const config = {
  style: "PRELOAD",
  auto_advance: true,
  response_time: 1000,
  continue_label: "Continue",
  show_continue_button: true,
};

export const Default = {
  args: {
    html: {
      body: "<p>This is <u>the</u> <b>HTML</b> <i>body</i></p>",
    },
    config: config,
    playback: playbackArgs,
    feedback_form: feedbackForm,
    onNext: () => {},
    onResult: () => {},
  },
};

export const BooleanColorScheme = {
  args: {
    ...Default.args,
    config: { ...config, style: undefined },
  },
};

export const NeutralColorScheme = {
  args: {
    ...BooleanColorScheme.args,
    feedback_form: {
      ...feedbackForm,
      form: [{ ...question1, style: { neutral: true } }, question2],
    },
  },
};

export const NeutralInvertedColorScheme = {
  args: {
    ...BooleanColorScheme.args,
    feedback_form: {
      ...feedbackForm,
      form: [{ ...question1, style: { "neutral-inverted": true } }, question2],
    },
  },
};

// Toontje hoger

const toontjeHogerPlaybackArgs = {
  sections: [
    {
      id: 2,
      url: "http://localhost:8000/section/2/13319/",
    },
    {
      id: 3,
      url: "http://localhost:8000/section/3/94320/",
    },
  ],
  play_method: "EXTERNAL",
  show_animation: false,
  preload_message: "",
  instruction: "",
  play_from: 0,
  mute: false,
  timeout_after_playback: null,
  stop_audio_after: 5,
  resume_play: false,
  style: { "neutral-inverted": true },
  ID: "MULTIPLAYER",
  view: "MULTIPLAYER",
  play_once: false,
  labels: ["A", "B"],
};

const toontjeHogerQuestion1 = {
  key: "pitch",
  view: "BUTTON_ARRAY",
  explainer: "",
  question: "Welk fragment heeft de juiste toonhoogte?",
  is_skippable: false,
  submits: true,
  style: { "neutral-inverted": true },
  choices: {
    A: "A",
    B: "B",
  },
  expected_response: "A",
};

export const ToontjeHoger4Absolute = {
  args: {
    ...Default.args,
    config: {
      ...config,
      response_time: 5,
      auto_advance: false,
      listen_first: false,
    },
    playback: toontjeHogerPlaybackArgs,
    feedback_form: {
      ...feedbackForm,
      form: [toontjeHogerQuestion1],
      is_skippable: false,
    },
  },
};
