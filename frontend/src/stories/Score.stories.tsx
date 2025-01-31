import { BrowserRouter as Router } from "react-router-dom";

import Score from "../components/Score/Score";

export default {
  title: "Score/Score",
  component: Score,
  parameters: {
    layout: "fullscreen",
  },
  argTypes: {
    scoreClass: {
      control: {
        type: "select",
      },
      options: ['diamond', 'platinum', 'gold', 'silver', 'bronze', 'plastic'],
    }
  }
};

function getScoreData(overrides = {}) {
  return {
    last_song: "Shania Twain - That don't impress me much",
    score: 100,
    score_message: "Correct!",
    total_score: 200,
    texts: {
      score: "Total score",
      next: "Next",
      listen_explainer: "You listened to:",
    },
    icon: "fa fa-music",
    feedback: "This is a feedback message",
    timer: setTimeout(() => { }, 1000),
    onNext: () => void 0,
    ...overrides,
  };
}

const getDecorator = (Story) => (
  <div
    style={{ width: "100%", height: "100%", backgroundColor: "#aaa", padding: "1rem" }}
  >
    <Router>
      <Story />
    </Router>
  </div>
);

export const Default = {
  args: getScoreData(),
  decorators: [getDecorator],
};

export const ZeroScore = {
  args: getScoreData({ score: 0, score_message: "No points!" }),
  decorators: [getDecorator],
};

export const NegativeScore = {
  args: getScoreData({ score: -100, score_message: "Incorrect!" }),
  decorators: [getDecorator],
};

export const ScoreWithoutLabel = {
  args: getScoreData({ score_message: "" }),
  decorators: [getDecorator],
};

export const CustomLabel = {
  args: getScoreData({ score_message: "points earned" }),
  decorators: [getDecorator],
};

export const CustomScoreClass = {
  args: getScoreData({ scoreClass: "silver" }),
  decorators: [getDecorator],
};

export const SelectableScoreClass = {
  args: getScoreData(),
  decorators: [getDecorator],
};
