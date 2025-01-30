import ProgressBar from "../components/ProgressBar/ProgressBar";

export default {
    title: "Progress/ProgressBar",
    component: ProgressBar,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        value: 50,
        max: 100,
        label: "3 / 20",
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
