import PlayButton from "../components/PlayButton/PlayButton";

export default {
    title: "Playback/PlayButton",
    component: PlayButton,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {},
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

export const Playing = {
    args: {
        isPlaying: true,
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

export const BooleanColorScheme = {
    args: {
        isPlaying: false,
        className: "boolean",
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

export const BooleanNegativeFirstColorScheme = {
    args: {
        isPlaying: false,
        className: "boolean-negative-first",
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

export const NeutralColorScheme = {
    args: {
        isPlaying: false,
        className: "neutral",
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

export const NeutralInvertedColorScheme = {
    args: {
        isPlaying: false,
        className: "neutral-inverted",
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
