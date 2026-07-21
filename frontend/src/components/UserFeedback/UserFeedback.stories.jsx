import UserFeedback from "./UserFeedback";

export default {
    title: "UserFeedback/UserFeedback",
    component: UserFeedback,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        blockIdentifier: "test",
        participant: "test",
        feedbackInfo: {
            header: "Feedback",
            button: "Submit",
            thank_you: "Thank you for your feedback!",
            contact_body:
                '<p>Please contact us at <a href="mailto:info@example.com">info@example.com</a> if you have any questions.</p>',
        },
        inline: true,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#fff", padding: "3rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const Vertical = {
    args: {
        blockIdentifier: "test",
        participant: "test",
        feedbackInfo: {
            header: "Feedback",
            button: "Submit",
            thank_you: "Thank you for your feedback!",
            contact_body:
                '<p>Please contact us at <a href="mailto:info@example.com">info@example.com</a> if you have any questions.</p>',
        },
        inline: false,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#fff", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};
