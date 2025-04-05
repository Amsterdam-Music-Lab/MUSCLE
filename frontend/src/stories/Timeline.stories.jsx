import Timeline, { getTimeline } from "../components/Timeline/Timeline";

const timeline = getTimeline(['star-4', 'dot', 'dot', 'star-5'])

export default {
    title: "Timeline/Timeline",
    component: Timeline,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        timeline: timeline,
    },
    decorators: [
        (Story) => (
            <div
                style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
            >
                <Story />
            </div>
        ),
    ],
};