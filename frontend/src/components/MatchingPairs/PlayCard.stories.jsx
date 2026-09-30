import PlayCard from "./PlayCard";
import useBoundStore from "@/util/stores";

export default {
    title: "MatchingPairs/PlayCard",
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
        link: "http://localhost:6006/audio/music.ogg",
        color: "colorPrimary",
    },
    showAnimation: true,
    view: "MATCHINGPAIRS",
    ...overrides,
});

const DefaultDecorator = (Story) => {
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme({colorPrimary:  '#d843e2', colorSecondary: '#39d7b8', colorPositive: '#39d7b8', colorNegative: '#fa5577', colorNeutral1: '#ffb14c', colorGrey: "#bbb"});
    return (
        <div
            style={{
                width: "256px",
                height: "256px",
                backgroundColor: "#ddd",
                color: "white",
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
            link: "http://localhost:6006/audio/music.ogg",
            turned: true,
        },
    }),
    decorators: [DefaultDecorator],
};

export const Seen = {
    args: getDefaultArgs({
        section: {
            link: "http://localhost:6006/audio/music.ogg",
            seen: true,
        },
    }),
    decorators: [DefaultDecorator],
};

export const Memory = {
    args: getDefaultArgs({
        section: {
            link: "http://localhost:6006/audio/music.ogg",
            memory: true,
        },
    }),
    decorators: [DefaultDecorator],
};

export const Lucky = {
    args: getDefaultArgs({
        section: {
            link: "http://localhost:6006/audio/music.ogg",
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
            link: "http://localhost:6006/audio/music.ogg",
            turned: true,
            playMethod: 'EXTERNAL'
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
            link: "http://localhost:6006/images/experiments/visual-matching-pairs/panther.jpg",
            turned: true,
            playMethod: 'NOAUDIO'
        },
    }),
    decorators: [DefaultDecorator],
};
