import PlayerSmall from "../components/PlayButton/PlayerSmall";

export default {
    title: "Playback/PlayerSmall",
    component: PlayerSmall,
    parameters: {
        layout: "fullscreen",
    },
};

export const Default = {
    args: {
        label: "Default",
        onClick: () => {
            alert("Default");
        },
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

export const Playing = {
    args: {
        label: "Playing",
        onClick: () => {
            alert("Playing");
        },
        playing: true,
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

export const Disabled = {
    args: {
        label: "Disabled",
        onClick: () => {
            alert("Disabled");
        },
        disabled: true,
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
