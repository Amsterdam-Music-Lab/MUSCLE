import PlayButton from "../components/PlayBack/PlayButton";
import useBoundStore from "@/util/stores";

export default {
    title: "Playback/PlayButton",
    component: PlayButton,
    parameters: {
        layout: "fullscreen",
    },
};

const SharedDecorator = (Story) => {
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme({ colorPrimary: '#d843e2', colorNeutral1: '#ffb14c', colorNeutral2: "#0cc7f1", colorNeutral3: "#2b2bee"});
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
    section: { link: audio, label: 'Play Button label', color: 'colorPrimary', playMethod: 'BUFFER', playFrom: 0.0 },
    view: 'BUTTON',
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
        section: { link: audio, label: 'Play Button label', color: 'colorNeutral1', playMethod: 'BUFFER', playFrom: 0.0 }
    }),
    decorators: [SharedDecorator],
};
