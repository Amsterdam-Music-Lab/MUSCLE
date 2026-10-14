import Trophy from "./Trophy";

export default {
    title: "Trophy/Trophy",
    component: Trophy,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        className: "gold",
        label: "Gold!"
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#9e9fa1", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};