import VisualMatchingPairs from '../components/MatchingPairs/MatchingPairs2';

import Cat01 from './assets/images/cat-01.webp';
import Cat02 from './assets/images/cat-02.webp';
import Cat03 from './assets/images/cat-03.webp';

export default {
    title: 'VisualMatchingPairs',
    component: VisualMatchingPairs,
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
            url: Cat01,
            turned: false,
            lucky: false,
            memory: false,
            group: 1,
        },
        {
            id: 2,
            url: Cat02,
            turned: false,
            lucky: false,
            memory: false,
            group: 2,
        },
        {
            id: 3,
            url: Cat03,
            turned: false,
            lucky: false,
            memory: false,
            group: 3,
        },
        {
            id: 4,
            url: Cat02,
            turned: false,
            lucky: false,
            memory: false,
            group: 2,
        },
        {
            id: 5,
            url: Cat01,
            turned: false,
            lucky: false,
            memory: false,
            group: 1,
        },
        {
            id: 6,
            url: Cat03,
            turned: false,
            lucky: false,
            memory: false,
            group: 3,
        },
    ],
    playerIndex: 0,
    stopAudio: () => { },
    submitResult: (args) => { alert('submitResult: ' + JSON.stringify(args, null, 2)); },
    finishedPlaying: () => { console.log('finished playing') },
    setPlayerIndex: (i) => { console.log('set player index', i) },
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

export const MoreCards = {
    args: {
        ...getDefaultArgs({
            sections: [
                {
                    id: 1,
                    url: Cat01,
                    turned: false,
                    lucky: false,
                    memory: false,
                    group: 1,
                },
                {
                    id: 2,
                    url: Cat02,
                    turned: false,
                    lucky: false,
                    memory: false,
                    group: 2,
                },
                {
                    id: 3,
                    url: Cat03,
                    turned: false,
                    lucky: false,
                    memory: false,
                    group: 3,
                },
                {
                    id: 4,
                    url: Cat02,
                    turned: false,
                    lucky: false,
                    memory: false,
                    group: 2,
                },
                {
                    id: 5,
                    url: Cat01,
                    turned: false,
                    lucky: false,
                    memory: false,
                    group: 1,
                },
                {
                    id: 6,
                    url: Cat03,
                    turned: false,
                    lucky: false,
                    memory: false,
                    group: 3,
                },
                {
                    id: 7,
                    url: Cat01,
                    turned: false,
                    lucky: false,
                    memory: false,
                    group: 1,
                },
                {
                    id: 8,
                    url: Cat02,
                    turned: false,
                    lucky: false,
                    memory: false,
                    group: 2,
                },
                {
                    id: 9,
                    url: Cat03,
                    turned: false,
                    lucky: false,
                    memory: false,
                    group: 3,
                },
                {
                    id: 10,
                    url: Cat02,
                    turned: false,
                    lucky: false,
                    memory: false,
                    group: 2,
                },
                {
                    id: 11,
                    url: Cat01,
                    turned: false,
                    lucky: false,
                    memory: false,
                    group: 1,
                },
                {
                    id: 12,
                    url: Cat03,
                    turned: false,
                    lucky: false,
                    memory: false,
                    group: 3,
                },
            ],
        }),
    },
    decorators: [
        (Story) => (
            <div id="root" style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding:'1rem' }}>
                <Story />
            </div>
        ),  
    ],
    parameters: {
        docs: {
            description: {
                component: 'This story shows the component with more cards.',
            },
        },
    },
};