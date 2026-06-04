import PlayButton from "../components/PlayBack/PlayButton";
import useBoundStore from "@/util/stores";
import music from "./assets/music.ogg";

export default {
    title: "Playback/PlayButton",
    component: PlayButton,
    parameters: {
        layout: "fullscreen",
    },
};

const SharedDecorator = (Story) => {
    const theme = { colorPrimary: '#d843e2', colorNeutral1: '#ffb14c', colorNeutral2: "#0cc7f1", colorNeutral3: "#2b2bee"};
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme(theme);
    return (
        <div
            style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
        >
            <Story />
        </div>
    )
};

const defaultArgs = {
    playSection: () => {},
    section: { link: music, label: 'LABEL', color: 'colorPrimary', playMethod: 'EXTERNAL', playFrom: 0.0 },
    view: 'BUTTON',
    isPlaying: false,
}

const getArgs = (overrides = {}) => ({
    ...defaultArgs,
    ...overrides
})

export const Default = {
    args: getArgs(),
    decorators: [SharedDecorator],
};

export const Playing = {
    args: getArgs({
        isPlaying: true,
    }),
    decorators: [SharedDecorator],
};

export const ChangedColor = {
    args: getArgs({
        isPlaying: false,
        section: { link: music, label: 'LABEL', color: 'colorNeutral1', playMethod: 'EXTERNAL', playFrom: 0.0 }
    }),
    decorators: [SharedDecorator],
};
