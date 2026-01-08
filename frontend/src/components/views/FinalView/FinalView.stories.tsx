/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { NarrowLayout } from "components/layout";
import FinalView from "./FinalView";

export default {
  title: "App/Views/FinalView",
  component: FinalView,
  decorators: [
    (Story) => (
      <NarrowLayout>
        <Story />
      </NarrowLayout>
    ),
  ],
  parameters: {
    backgrounds: {
      values: [{ value: "#ddd" }],
    },
  },
};

const shareConfig = {
  channels: ["facebook", "whatsapp", "twitter", "weibo", "share", "clipboard"],
  url: "https://www.example.com",
  content: "Hey! Check out this cool experiment",
  tags: ["coolexperiment", "awesome"],
};

const timeline = {
  currentStep: 4,
  symbols: [
    "dot",
    "dot",
    "star-4",
    "dot",
    "dot",
    "star-5",
    "dot",
    "dot",
    "star-6",
  ],
};

export const Default = {
  args: {
    score: 100,
    totalScore: 1234,
    percentile: 66,
    overallPercentile: 12,
    button: {
      // text: "Button",
      link: "https://www.example.com",
    },
    social: shareConfig,
    show_profile_link: true,
    action_texts: {
      all_experiments: "All experiments",
      profile: "Profile",
    },
    show_participant_link: true,
    participant_id_only: false,
    // feedback_info: {
    //   header: "Feedback",
    //   button: "Submit",
    //   thank_you: "Thank you for your feedback!",
    //   contact_body:
    //     '<p>Please contact us at <a href="mailto:info@example.com">',
    // },
    timeline,
    block: {
      slug: "test",
    },
    participant: "test",
    onNext: () => {
      alert("Next");
    },

    trophyContent: {
      default: {
        header: "Yay, you've earned a star! 💫",
        body: "Play on and collect 'm all...",
      },
      first: {
        header: "Congrats! You've earned your first star! 💫",
        body: "Can you collect them all?",
      },
      last: {
        header: "🎉 Woohoo! You've collected all stars!",
        body: "Play on? Let's start another round of games...",
      },
    },
  },
};

// with relative button.link
export const RelativeButtonLink = {
  args: {
    ...Default.args,
    button: {
      text: "Play again",
      link: "/profile",
    },
  },
};

export const FirstTrophy = {
  args: { ...Default.args, timeline: { ...timeline, currentStep: 3 } },
};

export const TimelineCompleted = {
  args: {
    ...Default.args,
    timeline: { ...timeline, currentStep: timeline.symbols.length },
  },
};

export const CustomPlugins = {
  args: {
    ...Default.args,
    plugins: [
      { name: "scoreboard", args: { plugins: [{ name: "overall-ranking" }] } },
    ],
  },
};
