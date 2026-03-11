import { http, HttpResponse } from 'msw'
import useBoundStore from "@/util/stores";
import MatchingPairs, { SCORE_FEEDBACK_DISPLAY } from "../components/MatchingPairs/MatchingPairs";
import { API_BASE_URL } from '@/config';
import { URLS } from '@/API';
import Cat01 from "./assets/images/cat-01.webp";
import Cat02 from "./assets/images/cat-02.webp";
import Cat03 from "./assets/images/cat-03.webp";
import music from "./assets/music.ogg";

const StoreDecorator = (Story) => {
    const setSession = useBoundStore((state) => state.setSession);
    const setParticipant = useBoundStore((state) => state.setParticipant);
    const setBlock = useBoundStore((state) => state.setBlock);
    const setTheme = useBoundStore((state) => state.setTheme);
    const theme =  {colorPrimary:  '#d843e2', colorSecondary: '#39d7b8', colorPositive: '#39d7b8', colorNegative: '#fa5577', colorNeutral1: '#ffb14c', colorGrey: "#bbb"};
    setSession({ id: 1 });
    setParticipant({ id: 1, csrf_token: "123" });
    setBlock({slug: 'test', theme: theme});
    setTheme(theme);

    return (
        <div
            id="root"
            style={{ width: "100%", height: "100%", backgroundColor: "#ddd", color: "white", padding: "1rem" }}
        >
            <Story />
        </div>
    );
};

export default {
    title: "MatchingPairs/MatchingPairs",
    component: MatchingPairs,
    parameters: {
        layout: "fullscreen",
        docs: {
            description: {
                component: "This story shows the component with the default props.",
                story: "This story shows the component with the default props.",
            },
        },
    },
};

const getDefaultArgs = (overrides = {}, nSections = 8) => ({
    playSection: () => { },
    sections: Array.from(new Array(nSections), (_) => { return {
        link: music,
        turned: false,
        lucky: false,
        memory: false,
        playMethod: "BUFFER"
    }}),
    playerIndex: 0,
    stopAudio: () => { },
    submitResult: () => { },
    finishedPlaying: () => { },
    ...overrides,
});

const getDefaultParams = (overrides = {}) => ({
    msw: {
        handlers: [
            http.post(API_BASE_URL + URLS.result.intermediateScore, () => {
                return HttpResponse.json({ score: 10 });
            })
        ],
    },
    ...overrides,
});

export const Default = {
    args: {
        ...getDefaultArgs(),
    },
    decorators: [StoreDecorator],
    parameters: getDefaultParams({
        docs: {
            description: {
                component: "This story shows the component with the default props.",
            },
        },
    }),
};

export const WithThreeColumns = {
    args: getDefaultArgs({}, 4),
    decorators: [StoreDecorator],
    parameters: getDefaultParams({
        docs: {
            description: {
                component:
                    "This story shows the component with three columns. The component automatically adjusts the number of columns based on the number of sections. Six or less sections will result in three columns, more than six sections will result in four columns.",
            },
        },
    }),
};

export const WithSmallBottomRightScoreFeedback = {
    args: {
        ...getDefaultArgs(),
        scoreFeedbackDisplay: SCORE_FEEDBACK_DISPLAY.SMALL_BOTTOM_RIGHT,
    },
    decorators: [StoreDecorator],
    parameters: getDefaultParams({
        docs: {
            description: {
                component: "This story shows the component with different positioning of feedback text",
            },
        },
    }),
};

export const WithShowAnimation = {
    args: {
        ...getDefaultArgs(),
        showAnimation: true,
    },
    decorators: [StoreDecorator],
    parameters: getDefaultParams({
        docs: {
            description: {
                component: "This story shows the component with animation of the turned cards",
            },
        },
    }),
};

export const VisualMatchingPairs = {
    args: getDefaultArgs({sections: [
        {
            link: `http://localhost:6006${Cat01}`,
            playMethod: 'NOAUDIO'
        },
        {
            link: `http://localhost:6006${Cat02}`,
            playMethod: 'NOAUDIO'
        },
        {
            link: `http://localhost:6006${Cat03}`,
            playMethod: 'NOAUDIO'
        },
        {
            link: `http://localhost:6006${Cat02}`,
            playMethod: 'NOAUDIO'
        },
        {
            link: `http://localhost:6006${Cat01}`,
            playMethod: 'NOAUDIO'
        },
        {
            link: `http://localhost:6006${Cat03}`,
            playMethod: 'NOAUDIO'
        },
    ]}),
    decorators: [StoreDecorator],
    parameters: getDefaultParams({
            docs: {
                description: {
                    component: "This story shows the component with visual stimuli.",
                },
            },
        }),
    
}

