import { BrowserRouter as Router } from "react-router-dom";

import Score from "./Score";
import useBoundStore from "@/util/stores";

const theme = { colorPositive: '#00b612', colorNegative: '#fa5577', colorGrey: '#bdbebf'};

const StoreDecorator = (Story) => {
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme(theme);
};

export default {
  title: "Score/Score",
  component: Score,
  parameters: {
    layout: "fullscreen",
  },
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
    feedback: "This is a feedback message",
    timer: setTimeout(() => { }, 1000),
    onNext: () => void 0,
    ...overrides,
  };
}

const getDecorator = (Story) => {
  StoreDecorator(); 
  return (
    <div
      style={{ width: "100%", height: "100%", backgroundColor: "#aaa", padding: "1rem" }}
    >
      <Router>
        <Story />
      </Router>
    </div>
  )
};

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
