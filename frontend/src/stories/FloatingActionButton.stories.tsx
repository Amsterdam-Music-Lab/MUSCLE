import UserFeedback from "@/components/UserFeedback/UserFeedback";
import FloatingActionButton from "@/components/FloatingActionButton/FloatingActionButton";

export default {
    title: "FloatingActionButton/FloatingActionButton",
    component: FloatingActionButton,
    parameters: {
        layout: "fullscreen",
    },
};

const userFeedbackProps = {
    blockSlug: "test",
    participant: "test",
    feedbackInfo: {
        header: "Feedback",
        button: "Submit",
        thank_you: "Thank you for your feedback!",
        contact_body:
            '<p>Please contact us at <a href="mailto:info@example.com">info@example.com</a> if you have any questions.</p>',
    },
    inline: false,
};

export const Default = {
    args: {
        children: <UserFeedback {...userFeedbackProps} />,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#aaa", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const TopLeft = {
    args: {
        position: "top-left",
        children: <UserFeedback {...userFeedbackProps} />,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#aaa", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const TopRight = {
    args: {
        position: "top-right",
        children: <UserFeedback {...userFeedbackProps} />,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#aaa", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const BottomLeft = {
    args: {
        position: "bottom-left",
        children: <UserFeedback {...userFeedbackProps} />,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#aaa", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const BottomRight = {
    args: {
        position: "bottom-right",
        children: <UserFeedback {...userFeedbackProps} />,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#aaa", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const CenterLeft = {
    args: {
        position: "center-left",
        children: <UserFeedback {...userFeedbackProps} />,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#aaa", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};

export const CenterRight = {
    args: {
        position: "center-right",
        children: <UserFeedback {...userFeedbackProps} />,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#aaa", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};
