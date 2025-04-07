import Timeline, { getTimeline } from "./Timeline";

const timeline = getTimeline({
    symbols: ['dot', 'dot', 'star-4', 'dot', 'dot', 'star-5', 'dot', 'dot', 'star-6'],
})

const timeline2 = getTimeline({
    symbols: ['star-5', 'dot', 'star-4', 'dot', 'dot', 'star-7', 'dot', 'dot', 'dot', 'star-8'],
})

const decorator = (Story) => (
    <div style={{ padding: "1rem", background: "#f5f5f5" }}>
        <Story />
    </div>
);

export default {
    title: "Game UI/Timeline",
    component: Timeline,
    parameters: {
        layout: "fullscreen",
    },
    tags: ["autodocs"]
};

export const Default = {
    args: {
        timeline: timeline,
        step: 4,
    },
    decorators: [decorator]
};

export const Alternative = {
    args: {
        timeline: timeline2,
        step: 7,
    },
    decorators: [decorator]
};


export const FancyFill = {
    args: {
        timeline: timeline,
        step: 4,
        fillPast: { startColor: "#ff0000", endColor: "#0000ff", scale: 2, angle: 60 }
    },
    decorators: [decorator]
};

export const NoSymbols = {
    args: {
        timeline: timeline,
        step: 5,
        showSymbols: false,
    },
    decorators: [decorator]
};

export const NoSpine = {
    args: {
        timeline: timeline,
        step: 5,
        showSpine: false,
    },
    decorators: [decorator]
};