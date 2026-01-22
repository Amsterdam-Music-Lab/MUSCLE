import PlayCard from "../components/MatchingPairs/PlayCard";
import catImage from "./assets/images/cat-01.webp";

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
        link: "/section/32/78165/",
        color: "colorPrimary",
    },
    showAnimation: true,
    view: "MATCHINGPAIRS",
    ...overrides,
});

const DefaultDecorator = (Story) => {
    return (
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
    )
}

export const Default = {
    args: getDefaultArgs(),
    decorators: [DefaultDecorator],
};

export const Turned = {
    args: getDefaultArgs({
        section: {
            id: 32,
            url: "/section/32/78165/",
            turned: true,
        },
    }),
    decorators: [DefaultDecorator],
};

export const Seen = {
    args: getDefaultArgs({
        section: {
            id: 32,
            url: "/section/32/78165/",
            seen: true,
        },
    }),
    decorators: [DefaultDecorator],
};

export const Memory = {
    args: getDefaultArgs({
        section: {
            id: 32,
            url: "/section/32/78165/",
            memory: true,
        },
    }),
    decorators: [DefaultDecorator],
};

export const Lucky = {
    args: getDefaultArgs({
        section: {
            id: 32,
            url: "/section/32/78165/",
            lucky: true,
        },
    }),
    decorators: [DefaultDecorator],
};

export const NoEvents = {
    args: getDefaultArgs({
        section: {
            noevents: true,
        },
    }),
    decorators: [DefaultDecorator],
};

export const Inactive = {
    args: getDefaultArgs({
        section: {
            inactive: true,
        },
    }),
    decorators: [DefaultDecorator],
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
    decorators: [DefaultDecorator],
};

export const VisualMatchingPairs = {
    args: getDefaultArgs({
        onClick: () => alert("Clicked!"),
        registerUserClicks: () => alert("Registered"),
        playing: false,
        section: {
            link: `http://localhost:6006/${catImage}`,
            turned: true,
        },
        view: "MATCHINGPAIRS",
    }),
    decorators: [DefaultDecorator],
};
