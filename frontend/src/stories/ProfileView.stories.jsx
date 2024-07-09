import { BrowserRouter as Router } from "react-router-dom";

import { ProfileView } from "../components/Profile/Profile";

export default {
    title: "ProfileView",
    component: ProfileView,
    parameters: {
        layout: "fullscreen",
    },
};

function getProfileData(overrides = {}) {
    return {
        messages: {
            title: "Profile",
            summary: "Knorrum bipsum sulfur bit dalmatian",
        },
        scores: [
            {
                finished_at: "2021-09-20T12:00:00Z",
                rank: {
                    class: "silver",
                    text: "2nd",
                },
                score: 100,
                points: "points",
                date: "2021-09-20",
                block_slug: "block-slug",
            },
            {
                finished_at: "2021-09-21T12:00:00Z",
                rank: {
                    class: "bronze",
                    text: "3rd",
                },
                score: 50,
                points: "points",
                date: "2021-09-21",
                block_slug: "block-slug",
            },
        ],
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
    args: getProfileData(),
    decorators: [getDecorator],
};
