import { BrowserRouter as Router } from "react-router-dom";

import ProfileView from "../components/Profile/ProfileView";

export default {
    title: "Profile/ProfileView",
    component: ProfileView,
    parameters: {
        layout: "fullscreen",
    },
};

function getProfileData(overrides = {}) {
    return {
        messages: {
            title: "Profile",
            summary: "You have participated in 6 Amsterdam Music Lab experiments. Your best scores are:",
            points: "points",
        },
        scores: [
            {
                finished_at: "2021-09-20T12:00:00Z",
                rank: {
                    class: "diamond",
                    text: "1st",
                },
                score: '250',
                date: "Never",
                block_slug: "block-slug",
            },
            {
                finished_at: "2021-09-20T12:00:00Z",
                rank: {
                    class: "platinum",
                    text: "1st",
                },
                score: '200',
                date: "Tomorrow",
                block_slug: "block-slug",
            },
            {
                finished_at: "2021-09-20T12:00:00Z",
                rank: {
                    class: "gold",
                    text: "1st",
                },
                score: '150',
                date: "Ereyesterday",
                block_slug: "block-slug",
            },
            {
                finished_at: "2021-09-20T12:00:00Z",
                rank: {
                    class: "silver",
                    text: "2nd",
                },
                score: '100',
                date: "Yesterday",
                block_slug: "block-slug",
            },
            {
                finished_at: "2021-09-21T12:00:00Z",
                rank: {
                    class: "bronze",
                    text: "3rd",
                },
                score: 50,
                date: "Today",
                block_slug: "block-slug",
            },
            {
                finished_at: "2021-09-20T12:00:00Z",
                rank: {
                    class: "plastic",
                    text: "100th",
                },
                score: '2',
                date: "Last year",
                block_slug: "block-slug",
            },
        ],
        ...overrides,
    };
}


const getDecorator = (Story) => (
    <div
        style={{ width: "100%", height: "100%", backgroundColor: "#333", padding: "1rem" }}
        className="aha__page aha__profile"
    >
        <div className="container">
            <div className="row justify-content-center">
                <div className="col-12">
                    <Router>
                        <Story />
                    </Router>
                </div>
            </div>
        </div>
    </div>
);

export const Default = {
    args: getProfileData(),
    decorators: [getDecorator],
};

export const NoScores = {
    args: getProfileData({
        messages: {
            title: "Profile",
            summary: "You have not participated in any Amsterdam Music Lab experiments yet.",
            points: "points",
        },
        scores: []
    }),
    decorators: [getDecorator],
};

export const SingleScore = {
    args: getProfileData({
        messages: {
            title: "Profile",
            summary: "You have participated in 1 Amsterdam Music Lab experiment. Your best score is:",
            points: "points",
        },
        scores: [
            {
                finished_at: "2021-09-20T12:00:00Z",
                rank: {
                    class: "gold",
                    text: "1nd",
                },
                score: '150',
                date: "Eergisteren",
                block_slug: "block-slug",
            },
        ],
    }),
    decorators: [getDecorator],
};

export const TwoScores = {
    args: getProfileData({
        scores: [
            {
                finished_at: "2021-09-20T12:00:00Z",
                rank: {
                    class: "gold",
                    text: "1nd",
                },
                score: '150',
                date: "Eergisteren",
                block_slug: "block-slug",
            },
            {
                finished_at: "2021-09-20T12:00:00Z",
                rank: {
                    class: "silver",
                    text: "2nd",
                },
                score: '100',
                date: "Gisteren",
                block_slug: "block-slug",
            },
        ],
    }),
    decorators: [getDecorator],
}
