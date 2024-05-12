import { BrowserRouter as Router } from "react-router-dom";

import Final from "../components/Final/Final";

export default {
    title: "Final",
    component: Final,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        score: 100,
        rank: {
            text: "Rank",
            class: "rank",
        },
        final_text: "<p>Final text</p>",
        points: "points",
        button: {
            text: "Button",
            link: "https://www.google.com",
        },
        logo: {
            image: "https://via.placeholder.com/150",
            link: "https://www.google.com",
        },
        social: {
            apps: ["facebook", "whatsapp", "twitter", "weibo", "share", "clipboard"],
            url: "https://www.google.com",
            message: "Message",
            hashtags: ["hashtag"],
            text: "Text",
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
                '<p>Please contact us at <a href="mailto:info@example.com">info@example.com</a> if you have any questions.</p>',
        },
        experiment: {
            slug: "test",
        },
        participant: "test",
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#aaa", padding: "1rem" }}
            >
                <Router>
                    <Story />
                </Router>
            </div>
        ),
    ],
};
