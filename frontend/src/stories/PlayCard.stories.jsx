import PlayCard from "../components/MatchingPairs/PlayCard";
import catImage from "./assets/images/cat-01.webp";

console.log(catImage);

export default {
    title: "Playback/PlayCard",
    component: PlayCard,
    parameters: {
        layout: "fullscreen",
    },
};

const getDefaultArgs = (overrides = {}) => ({
    onClick: () => alert("Clicked!"),
    registerUserClicks: () => void 0,
    playing: true,
    section: {
        id: 32,
        url: "/section/32/78165/",
    },
    showAnimation: true,
    view: "MATCHINGPAIRS",
    ...overrides,
});

export const Default = {
    args: getDefaultArgs(),
    decorators: [
        (Story) => (
            <div
                style={{
                    width: "256px",
                    height: "256px",
                    backgroundColor: "#ddd",
                    padding: "1rem",
                }}
            >
                <Story />
            </div>
        ),
    ],
};

export const Turned = {
    args: getDefaultArgs({
        section: {
            id: 32,
            url: "/section/32/78165/",
            turned: true,
        },
    }),
    decorators: [
        (Story) => (
            <div
                style={{
                    width: "256px",
                    height: "256px",
                    backgroundColor: "#ddd",
                    padding: "1rem",
                }}
            >
                <Story />
            </div>
        ),
    ],
};

export const Seen = {
    args: getDefaultArgs({
        section: {
            id: 32,
            url: "/section/32/78165/",
            seen: true,
        },
    }),
    decorators: [
        (Story) => (
            <div
                style={{
                    width: "256px",
                    height: "256px",
                    backgroundColor: "#ddd",
                    padding: "1rem",
                }}
            >
                <Story />
            </div>
        ),
    ],
};

export const Memory = {
    args: getDefaultArgs({
        section: {
            id: 32,
            url: "/section/32/78165/",
            memory: true,
        },
    }),
    decorators: [
        (Story) => (
            <div
                style={{
                    width: "256px",
                    height: "256px",
                    backgroundColor: "#ddd",
                    padding: "1rem",
                }}
            >
                <Story />
            </div>
        ),
    ],
};

export const Lucky = {
    args: getDefaultArgs({
        section: {
            id: 32,
            url: "/section/32/78165/",
            lucky: true,
        },
    }),
    decorators: [
        (Story) => (
            <div
                style={{
                    width: "256px",
                    height: "256px",
                    backgroundColor: "#ddd",
                    padding: "1rem",
                }}
            >
                <Story />
            </div>
        ),
    ],
};

export const NoEvents = {
    args: getDefaultArgs({
        section: {
            id: 32,
            url: "/section/32/78165/",
            noevents: true,
        },
    }),
    decorators: [
        (Story) => (
            <div
                style={{
                    width: "256px",
                    height: "256px",
                    backgroundColor: "#ddd",
                    padding: "1rem",
                }}
            >
                <Story />
            </div>
        ),
    ],
};

export const Inactive = {
    args: getDefaultArgs({
        section: {
            id: 32,
            url: "/section/32/78165/",
            inactive: true,
        },
    }),
    decorators: [
        (Story) => (
            <div
                style={{
                    width: "256px",
                    height: "256px",
                    backgroundColor: "#ddd",
                    padding: "1rem",
                }}
            >
                <Story />
            </div>
        ),
    ],
};

export const Playing = {
    args: getDefaultArgs({
        onClick: () => void 0,
        registerUserClicks: () => void 0,
        playing: true,
        showAnimation: true,
        section: {
            id: 32,
            url: "/section/32/78165/",
            turned: true,
        },
    }),
    decorators: [
        (Story) => (
            <div
                style={{
                    width: "128px",
                    minHeight: "128px",
                    margin: "1rem auto",
                    height: "256px",
                    backgroundColor: "#ddd",
                    padding: "1rem",
                }}
            >
                <Story />
            </div>
        ),
    ],
};

export const VisualMatchingPairs = {
    args: getDefaultArgs({
        onClick: () => alert("Clicked!"),
        registerUserClicks: () => alert("Registered"),
        playing: false,
        section: {
            id: 32,
            url: `http://localhost:6006/${catImage}`,
            turned: true,
        },
        view: "MATCHINGPAIRS",
    }),
    decorators: [
        (Story) => (
            <div
                style={{
                    width: "256px",
                    height: "256px",
                    backgroundColor: "#ddd",
                    padding: "1rem",
                }}
            >
                <Story />
            </div>
        ),
    ],
};
