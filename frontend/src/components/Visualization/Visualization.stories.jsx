import Visualization from "./Visualization";

export default {
    title: "Visualization/Visualization",
    component: Visualization,
    parameters: {
        layout: "fullscreen",
    },
};

const getDecorator = (Story) => (
    <div
        style={{ width: "100%", height: "100%", backgroundColor: "#9e9fa1", padding: "1rem" }}
    >
        <Story />
    </div>
)

export const Default = {
    args: {
        className: "gold",
        type: "percentile",
        value: 80,
        label: "%"
    },
    decorators: [getDecorator]
};

export const ProgressBar = {
    args: {
        className: "bronze",
        type: "progress",
        value: 60,
        label: "%"
    },
    decorators: [getDecorator]
};