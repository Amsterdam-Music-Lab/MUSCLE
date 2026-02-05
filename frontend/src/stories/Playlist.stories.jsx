import { BrowserRouter as Router } from "react-router-dom";

import Playlist from "../components/Playlist/Playlist";

export default {
    title: "Playlist/Playlist",
    component: Playlist,
    parameters: {
        layout: "fullscreen",
    },
};

function getPlaylistData(overrides = {}) {
    return {
        messages: {
            title: "Profile",
            summary: "You have participated in 6 Amsterdam Music Lab experiments. Your best scores are:",
            points: "points",
        },
        scores: [
            {
                finished_at: "2021-09-20T12:00:00Z",
                rank: {
                    class: "diamond",
                    text: "1st",
                },
                score: '250',
                date: "Never",
                block_slug: "block-slug",
            },
            {
                finished_at: "2021-09-20T12:00:00Z",
                rank: {
                    class: "platinum",
                    text: "1st",
                },
                score: '200',
                date: "Tomorrow",
                block_slug: "block-slug",
            },
            {
                finished_at: "2021-09-20T12:00:00Z",
                rank: {
                    class: "gold",
                    text: "1st",
                },
                score: '150',
                date: "Ereyesterday",
                block_slug: "block-slug",
            },
            {
                finished_at: "2021-09-20T12:00:00Z",
                rank: {
                    class: "silver",
                    text: "2nd",
                },
                score: '100',
                date: "Yesterday",
                block_slug: "block-slug",
            },
            {
                finished_at: "2021-09-21T12:00:00Z",
                rank: {
                    class: "bronze",
                    text: "3rd",
                },
                score: 50,
                date: "Today",
                block_slug: "block-slug",
            },
            {
                finished_at: "2021-09-20T12:00:00Z",
                rank: {
                    class: "plastic",
                    text: "100th",
                },
                score: '2',
                date: "Last year",
                block_slug: "block-slug",
            },
        ],
        ...overrides,
    };
}


const getDecorator = (Story) => (
    <div
        style={{ width: "100%", height: "100%", backgroundColor: "#ddd", padding: "1rem" }}
    >
        <Story />
    </div>
);

export const Default = {
    args: {
        block: {
            slug: 'test',
            name: 'Test block',
            theme: {
                colorPrimary: 'teal'
            },
            playlists: [
                {id: 1, name: 'First playlist'},
                {id: 2, name: 'Second playlist'}
            ]
        }
    },
    decorators: [getDecorator],
};
