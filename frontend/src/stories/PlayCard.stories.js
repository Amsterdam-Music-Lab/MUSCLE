
import PlayCard from '../components/PlayButton/PlayCard';
import catImage from './assets/images/cat-01.webp';

console.log(catImage);

export default {
  title: 'PlayCard',
  component: PlayCard,
  parameters: {
    layout: 'fullscreen',
  },
};

export const Default = {
    args: {
        onClick: () => alert("Clicked!"),
        registerUserClicks: () => alert('Registered'),
        playing: false,
        section: {
            "id": 32,
            "url": "/section/32/78165/",
            "group": "\t1"
        },
        view: "MATCHINGPAIRS"
    },
    decorators: [
        (Story) => (
            <div style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
};

export const Turned = {
    args: {
        onClick: () => alert("Clicked!"),
        registerUserClicks: () => alert('Registered'),
        playing: false,
        section: {
            "id": 32,
            "url": "/section/32/78165/",
            "group": "\t1",
            "turned": true
        },
        view: "MATCHINGPAIRS"
    },
    decorators: [
        (Story) => (
            <div style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
};

export const Seen = {
    args: {
        onClick: () => alert("Clicked!"),
        registerUserClicks: () => alert('Registered'),
        playing: false,
        section: {
            "id": 32,
            "url": "/section/32/78165/",
            "group": "\t1",
            "seen": true
        },
        view: "MATCHINGPAIRS"
    },
    decorators: [
        (Story) => (
            <div style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
};

export const Memory = {
    args: {
        onClick: () => alert("Clicked!"),
        registerUserClicks: () => alert('Registered'),
        playing: false,
        section: {
            "id": 32,
            "url": "/section/32/78165/",
            "group": "\t1",
            "memory": true
        },
        view: "MATCHINGPAIRS"
    },
    decorators: [
        (Story) => (
            <div style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
};

export const Lucky = {
    args: {
        onClick: () => alert("Clicked!"),
        registerUserClicks: () => alert('Registered'),
        playing: false,
        section: {
            "id": 32,
            "url": "/section/32/78165/",
            "group": "\t1",
            "lucky": true
        },
        view: "MATCHINGPAIRS"
    },
    decorators: [
        (Story) => (
            <div style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
};

export const NoEvents = {
    args: {
        onClick: () => alert("Clicked!"),
        registerUserClicks: () => alert('Registered'),
        playing: false,
        section: {
            "id": 32,
            "url": "/section/32/78165/",
            "group": "\t1",
            "noevents": true
        },
        view: "MATCHINGPAIRS"
    },
    decorators: [
        (Story) => (
            <div style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
};

export const Inactive = {
    args: {
        onClick: () => alert("Clicked!"),
        registerUserClicks: () => alert('Registered'),
        playing: false,
        section: {
            "id": 32,
            "url": "/section/32/78165/",
            "group": "\t1",
            "inactive": true
        },
        view: "MATCHINGPAIRS"
    },
    decorators: [
        (Story) => (
            <div style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
};

export const Playing = {
    args: {
        onClick: () => void 0,
        registerUserClicks: () => void 0,
        playing: true,
        section: {
            "id": 32,
            "url": "/section/32/78165/",
            "group": "\t1",
            "turned": true
        },
        view: "MATCHINGPAIRS"
    },
    decorators: [
        (Story) => (
            <div style={{ display: 'flex', width: '100%', minHeight: '128px', height: '100%', backgroundColor: '#ddd', padding: '1rem'}}>
                <Story />
            </div>
        ),
    ],
};

export const VisualMatchingPairs = {
    args: {
        onClick: () => alert("Clicked!"),
        registerUserClicks: () => alert('Registered'),
        playing: false,
        section: {
            "id": 32,
            "url": `http://localhost:6006/${catImage}`,
            "group": "\t1",
            "turned": true
        },
        view: "VISUALMATCHINGPAIRS"
    },
    decorators: [
        (Story) => (
            <div style={{ width: '100%', height: '100%', backgroundColor: '#ddd', padding: '1rem' }}>
                <Story />
            </div>
        ),
    ],
};