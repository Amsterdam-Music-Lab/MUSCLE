import { BrowserRouter as Router } from "react-router-dom";

import Header from "../components/Experiment/Header/Header";

export default {
    title: "Header/Header",
    component: Header,
    parameters: {
        layout: "fullscreen",
    },
};

function getHeaderData(overrides = {}) {
    return {
        description: "<h1>Experiment ABC</h1><p>This is the experiment description</p>",
        nextBlockSlug: '/th1-mozart',
        nextBlockButtonText: 'Volgende experiment',
        experimentSlug: '/thkids',
        aboutButtonText: 'Over ons',
        totalScore: 420,
        scoreDisplayConfig: {
            scoreClass: 'gold',
            scoreLabel: 'points',
        },
        ...overrides,
    };
}

const getDecorator = (Story) => (
    <div
        className="aha__experiment"
        style={{ width: "100%", height: "100%", backgroundColor: "#aaa", padding: "1rem" }}
    >
        <Router>
            <Story />
        </Router>
    </div>
);

export const Default = {
    args: getHeaderData(),
    decorators: [getDecorator],
};

export const ZeroScore = {
    args: getHeaderData({ score: 0, score_message: "No points!" }),
    decorators: [getDecorator],
};

export const NegativeScore = {
    args: getHeaderData({ score: -100, score_message: "Incorrect!" }),
    decorators: [getDecorator],
};

export const ScoreWithoutLabel = {
    args: getHeaderData({ score_message: "" }),
    decorators: [getDecorator],
};

export const CustomLabel = {
    args: getHeaderData({ score_message: "points earned" }),
    decorators: [getDecorator],
};

export const CustomScoreClass = {
    args: getHeaderData({ scoreClass: "silver" }),
    decorators: [getDecorator],
};

export const SelectableScoreClass = {
    args: getHeaderData(),
    decorators: [getDecorator],
};
