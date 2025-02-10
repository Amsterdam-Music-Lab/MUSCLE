import { BrowserRouter as Router } from "react-router-dom";

import Rank from "../components/Rank/Rank";

export default {
    title: "Rank/Rank",
    component: Rank,
    parameters: {
        layout: "fullscreen",
    },
};

function getCupData(overrides = {}) {
    return {
        text: "Rank",
        className: "rank",
        ...overrides,
    };
}

function getScoreData(overrides = {}) {
    return {
        score: 100,
        label: "points",
        ...overrides,
    };
}

function getRankData(cupOverrides = {}, scoreOverrides = {}) {
    return {
        cup: getCupData(cupOverrides),
        score: getScoreData(scoreOverrides),
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
    args: getRankData(),
    decorators: [getDecorator],
};

export const SilverCup = {
    args: getRankData({ className: "rank silver" }),
    decorators: [getDecorator],
};

export const BronzeCup = {
    args: getRankData({ className: "rank bronze" }),
    decorators: [getDecorator],
};

export const NoCupText = {
    args: getRankData({ text: "" }),
    decorators: [getDecorator],
};

export const ZeroScore = {
    args: getRankData({ score: 0 }),
    decorators: [getDecorator],
};

export const NegativeScore = {
    args: getRankData({ score: -100 }),
    decorators: [getDecorator],
};

export const ScoreWithoutLabel = {
    args: getRankData({ label: "" }),
    decorators: [getDecorator],
};

export const CustomLabel = {
    args: getRankData({ label: "points earned" }),
    decorators: [getDecorator],
};
