/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import { t } from "@lingui/core/macro";
import type { FrontendConfig, ViewConfig } from "@/types/frontend";

export function config(): FrontendConfig {
  // Logo plugin
  const logo = {
    name: "logo",
    args: {
      name: "tunetwins",
      fill: "white",
    },
  };

  const disclaimerText = t`
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

  // Timeline used throughout the game
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
          args: { value: "https://tunetwins.app" },
        },
        {
          name: "markdown",
          args: {
            content: t`**Invite your friends to play!** Simply ask them to scan this QR code.`,
          },
        },
      ],
    },
  };

  const scoreboard = {
    name: "scoreboard",
    args: {
      plugins: [
        { name: "ranking" },
        { name: "scores" },
        {
          name: "timeline",
          args: { timeline: { symbols: timelineSymbols } },
          wrapperProps: { title: t`Your progress...` },
        },
        qrPluginSpec,
        { name: "share" },
      ],
    },
  };

  const landingText = t`
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
                title: t`Test Your Musical Memory!`,
                titleTag: "h2",
              },
              args: {
                content: landingText,
              },
            },

            {
              name: "markdown",
              wrapperProps: {
                title: t`Note:`,
              },
              args: {
                content: t`The first load may take a while due to the amount of content, but later runs will be smoother.`,
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
          children: t`Start the game!`,
        },
      },

      footer,
    ],
  };

  const finalView: ViewConfig = {
    plugins: [
      logo,
      { name: "trophy" },
      scoreboard,
      {
        name: "linkButton",
        args: {
          children: t`Play another game!`,
        },
      },
      footer,
    ],

    trophyContent: {
      default: {
        header: t`Yay, you've earned a star! 💫`,
        body: t`Play on and collect 'm all...`,
      },
      first: {
        header: t`Woohoo! You've earned your first star! 💫`,
        body: t`Can you collect them all?`,
      },
      last: {
        header: t`🎉 Amazing! You've finished the game!`,
        body: t`Play on? Let's start another round of games...`,
      },
    },
  };

  const tunetwinsView: ViewConfig = {
    timeline: { symbols: timelineSymbols },
  };

  return {
    showLanding: true,
    landing: landingView,
    final: finalView,
    tunetwins: tunetwinsView,
  };
}
