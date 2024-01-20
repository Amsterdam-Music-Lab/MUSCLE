import MatchingPairs, { SCORE_FEEDBACK_DISPLAY } from '../components/Playback/MatchingPairs';

import audio from './assets/audio.wav';

export default {
    title: 'MatchingPairs',
    component: MatchingPairs,
    parameters: {
        layout: 'fullscreen',
        docs: {
            description: {
                component: 'This story shows the component with the default props.',
                story: 'This story shows the component with the default props.',
            },
        }
    },
};

const getDefaultArgs = (overrides = {}) => ({
    playSection: () => { },
    sections: [
        {
            id: 1,
            url: audio,
            turned: false,
            lucky: false,
            memory: false,
        },
        {
            id: 2,
            url: audio,
            turned: false,
            lucky: false,
            memory: false,
        },
        {
            id: 3,
            url: audio,
            turned: false,
            lucky: false,
            memory: false,
        },
        {
            id: 4,
            url: audio,
            turned: false,
            lucky: false,
            memory: false,
        },
        {
            id: 5,
            url: audio,
            turned: false,
            lucky: false,
            memory: false,
        },
        {
            id: 6,
            url: audio,
            turned: false,
            lucky: false,
            memory: false,
        },
        {
            id: 7,
            url: audio,
            turned: false,
            lucky: false,
            memory: false,
        },
        {
            id: 8,
            url: audio,
            turned: false,
            lucky: false,
            memory: false,
        },
    ],
    playerIndex: 0,
    stopAudio: () => { },
    submitResult: () => { },
    finishedPlaying: () => { },
    ...overrides,
})

export const Default = {
    args: {
        ...getDefaultArgs(),
    },
    decorators: [
        (Story) => (
            <div id="root" style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
    parameters: {
        docs: {
            description: {
                component: 'This story shows the component with the default props.',
            },
        },
    },
};

export const WithThreeColumns = {
    args: getDefaultArgs({
        sections: [
            {
                id: 1,
                url: audio,
                turned: false,
                lucky: false,
                memory: false,
            },
            {
                id: 2,
                url: audio,
                turned: false,
                lucky: false,
                memory: false,
            },
            {
                id: 3,
                url: audio,
                turned: false,
                lucky: false,
                memory: false,
            },
            {
                id: 4,
                url: audio,
                turned: false,
                lucky: false,
                memory: false,
            },
            {
                id: 5,
                url: audio,
                turned: false,
                lucky: false,
                memory: false,
            },
            {
                id: 6,
                url: audio,
                turned: false,
                lucky: false,
                memory: false,
            },
        ],
    }),
    decorators: [
        (Story) => (
            <div id="root" style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
    parameters: {
        docs: {
            description: {
                component: 'This story shows the component with three columns. The component automatically adjusts the number of columns based on the number of sections. Six or less sections will result in three columns, more than six sections will result in four columns.',
            },
        },
    },
};

export const WithSmallBottomRightScoreFeedback = {
    args: {
        ...getDefaultArgs(),
        scoreFeedbackDisplay: SCORE_FEEDBACK_DISPLAY.SMALL_BOTTOM_RIGHT
    },
    decorators: [
        (Story) => (
            <div id="root" style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
    parameters: {
        docs: {
            description: {
                component: 'This story shows the component with the default props.',
            },
        },
    },
};