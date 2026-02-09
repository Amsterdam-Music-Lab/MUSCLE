import UserFeedback from "@/components/UserFeedback/UserFeedback";
import FloatingActionButton from "@/components/FloatingActionButton/FloatingActionButton";
import useBoundStore from "@/util/stores";

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
        button: {
            label: "Submit",
            color: "colorPrimary"
        },
        thank_you: "Thank you for your feedback!",
        contact_body:
            '<p>Please contact us at <a href="mailto:info@example.com">info@example.com</a> if you have any questions.</p>',
        show_float_button: true
    },
    inline: false,
};

const feedbackDecorator = (Story) => {
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme({ colorPrimary: "#d843e2", colorBackground: "black" });
    return (
        <div
            style={{ width: "100%", height: "100%", backgroundColor: "#aaa", padding: "1rem" }}
        >
            <Story />
        </div>
    )
}

export const Default = {
    args: {
        children: <UserFeedback {...userFeedbackProps} />,
    },
    decorators: [feedbackDecorator],
};

export const TopLeft = {
    args: {
        position: "top-left",
        children: <UserFeedback {...userFeedbackProps} />,
    },
    decorators: [feedbackDecorator],
};

export const TopRight = {
    args: {
        position: "top-right",
        children: <UserFeedback {...userFeedbackProps} />,
    },
    decorators: [feedbackDecorator],
};

export const BottomLeft = {
    args: {
        position: "bottom-left",
        children: <UserFeedback {...userFeedbackProps} />,
    },
    decorators: [feedbackDecorator],
};

export const BottomRight = {
    args: {
        position: "bottom-right",
        children: <UserFeedback {...userFeedbackProps} />,
    },
    decorators: [feedbackDecorator],
};

export const CenterLeft = {
    args: {
        position: "center-left",
        children: <UserFeedback {...userFeedbackProps} />,
    },
    decorators: [feedbackDecorator],
};

export const CenterRight = {
    args: {
        position: "center-right",
        children: <UserFeedback {...userFeedbackProps} />,
    },
    decorators: [feedbackDecorator],
};
