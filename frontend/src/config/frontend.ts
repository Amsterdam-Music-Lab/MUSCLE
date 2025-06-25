/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { FrontendConfig, ViewConfig } from "@/types/frontend";

// Logo plugin
const logo = {
  name: "logo",
  args: {
    name: "tunetwins",
    fill: "white",
  },
};

const disclaimerText = `
TuneTwins was created by members of the Music Cognition Group 
and supported by the Dutch Research Council and Faculty of Humanities at the University 
of Amsterdam. This website processes only anonymized data. For more information, 
see [UvA Privacy](https://www.uva.nl/en/home/disclaimers/privacy.html)`;

// Footer plugin
const footer = {
  name: "footer",
  args: {
    logos: ["nwo", "uva", "aml", "mcg"],
    disclaimer: disclaimerText,
  },
};

// Scoreboard plugin
const timelineSymbols = [
  "dot",
  "dot",
  "star-4",
  "dot",
  "dot",
  "star-5",
  "dot",
  "dot",
  "star-6",
  "dot",
  "dot",
  "star-7",
];

const qrPluginSpec = {
  name: "flex",
  args: {
    plugins: [
      {
        name: "qrcode",
        args: { value: "https://www.mcg.uva.nl/tunetwins/" },
      },
      {
        name: "markdown",
        args: {
          content:
            "**Invite your friends to play!** Simply ask them to scan this QR code.",
        },
      },
    ],
  },
};

const scoreboard = {
  name: "scoreboard",
  args: {
    plugins: [
      {
        name: "logo",
        enabled: false,
        args: { name: "tunetwins" },
      },

      // Ranking
      {
        // enabled: false,
        name: "ranking",
        enabled: true,
        args: {
          cutoff: 30,
          headerAboveCutoff:
            "Congrats! You did better than {{percentile}}% of players at this level!",
          headerBelowCuttoff:
            "Congrats! You did better than {{cutoff}}% of players at this level!",
        },
      },

      // Scores
      {
        name: "scores",
        args: {
          turnScoreLabel: "Last game",
          totalScoreLabel: "Total score",
          // variant: "primary",
        },
        wrapperProps: {
          // title: "Your scores...",
        },
      },

      // Timeline
      {
        name: "timeline",
        // order: 2,
        args: {
          timeline: { symbols: timelineSymbols },
          // dotSize: 15,
        },
        wrapperProps: {
          title: "Your progress...",
        },
      },
      qrPluginSpec,
      // Sharing options
      {
        name: "share",
        args: {
          label: "Share",
          // variant: "primary",
        },
      },
    ],
  },
};

const landingText = `
How good are you in memorizing music? 
Can you still remember tunes when some information is hidden?
Find out with **TuneTwins**, a science game from the University of Amsterdam. 
Match melodies, clear the board, and minimize mistakes!
`;

const landingView: ViewConfig = {
  plugins: [
    logo,
    {
      name: "card",
      args: {
        plugins: [
          {
            name: "logo",
            enabled: false,
            args: {
              name: "tunetwins",
              height: 3,
            },
          },
          {
            name: "markdown",
            wrapperProps: {
              title: "Test Your Musical Memory!",
              titleTag: "h2",
            },
            args: {
              content: landingText,
            },
          },

          // more components...
        ],
      },
    },
    {
      name: "linkButton",
      args: {
        // Actual link is added by the Landing component
        children: "Start the game!",
      },
    },

    footer,
  ],
};

const finalView: ViewConfig = {
  plugins: [
    logo,
    scoreboard,
    {
      name: "linkButton",
      args: {
        children: "Play another game!",
      },
    },
    {
      name: "userFeedback",
      // enabled: false,
      args: {
        // You cannot change this yet...
        // buttonText: "bla",
      },
    },
    footer,
  ],
};

export default {
  showLanding: true,
  landing: landingView,
  final: finalView,
  tunetwins: {
    timeline: { symbols: timelineSymbols },
  },
} as FrontendConfig;
