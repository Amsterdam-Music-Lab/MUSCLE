import { BrowserRouter as Router } from "react-router-dom";

import ScoreCounter from "../components/ScoreCounter/ScoreCounter";

export default {
  title: "Score/ScoreCounter",
  component: ScoreCounter,
  parameters: {
    layout: "fullscreen",
  },
};

function getScoreData(overrides = {}) {
  return {
    score: 100,
    label: "points",
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
  args: getScoreData({ score: 0 }),
  decorators: [getDecorator],
};

export const NegativeScore = {
  args: getScoreData({ score: -100 }),
  decorators: [getDecorator],
};

export const ScoreWithoutLabel = {
  args: getScoreData({ label: "" }),
  decorators: [getDecorator],
};

export const CustomLabel = {
  args: getScoreData({ label: "points earned" }),
  decorators: [getDecorator],
};
