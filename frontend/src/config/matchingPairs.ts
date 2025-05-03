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

const scoreboardPlugins = [
  {
    name: "logo",
    enabled: false,
    args: { name: "tunetwins" },
  },

  // Ranking
  {
    name: "ranking",
    // order: 0,
    // enabled: false,
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
    // order: 1,
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
      symbols: timelineSymbols,
      // dotSize: 15,
    },
    wrapperProps: {
      title: "Your progress...",
    },
  },

  // Sharing options
  {
    name: "share",
    args: {
      label: "Share",
      // variant: "primary",
    },
  },
];

const finalPlugins = [
  {
    name: "logo",
    args: {
      name: "tunetwins",
      fill: "white",
    },
  },
  {
    name: "scoreboard",
    args: {
      plugins: scoreboardPlugins,
    },
  },

  {
    name: "linkButton",
    args: {
      children: "bla",
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

  {
    name: "footer",
    args: {
      logos: ["nwo", "uva", "aml", "mcg"],
      disclaimer: "This is the disclaimer text.",
    },
  },
];

export const matchingPairsConfig = {
  final: {
    plugins: finalPlugins,
  },
};
