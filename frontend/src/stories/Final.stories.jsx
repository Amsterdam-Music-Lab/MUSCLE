import { BrowserRouter as Router } from "react-router-dom";

import Final from "../components/Final/Final";

export default {
    title: "Final",
    component: Final,
    parameters: {
        layout: "fullscreen",
    },
};

function getFinalData(overrides = {}) {
    return {
        score: 100,
        rank: {
            text: "Rank",
            class: "rank",
        },
        final_text: "<p>Final text</p>",
        points: "points",
        button: {
            text: "Button",
            link: "https://www.example.com",
        },
        logo: {
            image: "https://via.placeholder.com/150",
            link: "https://www.example.com",
        },
        social: {
            channels: ["facebook", "whatsapp", "twitter", "weibo", "share", "clipboard"],
            url: "https://www.example.com",
            content: "Hey! Check out this cool experiment",
            tags: ["coolexperiment", "awesome"],
        },
        show_profile_link: true,
        action_texts: {
            all_experiments: "All experiments",
            profile: "Profile",
        },
        show_participant_link: true,
        participant_id_only: false,
        feedback_info: {
            header: "Feedback",
            button: "Submit",
            thank_you: "Thank you for your feedback!",
            contact_body:
                '<p>Please contact us at <a href="mailto:info@example.com">',
        },
        block: {
            slug: "test",
        },
        participant: "test",
        onNext: () => { alert("Next"); },
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
    args: getFinalData(),
    decorators: [getDecorator],
};

// with relative button.link
export const RelativeButtonLink = {
    args: getFinalData({
        button: {
            text: "Play again",
            link: "/profile",
        },
    }),
    decorators: [getDecorator],
};

// with absolute button.link
export const AbsoluteButtonLink = {
    args: getFinalData({
        button: {
            text: "Button",
            link: "https://www.example.com",
        },
    }),
    decorators: [getDecorator],
};

// without button.link
export const NoButtonLink = {
    args: getFinalData({
        button: {
            text: "Button",
            link: "",
        },
    }),
    decorators: [getDecorator],
};
