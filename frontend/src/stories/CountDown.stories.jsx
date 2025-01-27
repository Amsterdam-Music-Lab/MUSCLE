import CountDown from "../components/CountDown/CountDown";

export default {
    title: "CountDown/CountDown",
    component: CountDown,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        duration: 3,
        running: true,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#666", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};
