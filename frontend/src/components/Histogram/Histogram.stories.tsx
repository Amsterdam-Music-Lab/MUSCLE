import type { Meta, StoryFn } from '@storybook/react';
import Histogram from "./Histogram";

const meta: Meta<typeof Histogram> = {
    title: "Game UI/Histogram",
    component: Histogram,
    parameters: {
        layout: "fullscreen",
    },
    tags: ["autodocs"],
};

const decorator = (Story: any) => (
    <div style={{ height: "200px", padding: "1rem" }}>
        <Story />
    </div>
)

export const Default = {
    args: {
        running: true,
    },
    decorators: [decorator]
};

export const Random = {
    args: {
        bars: 7,
        running: true,
        random: true,
        interval: 200,
    },
    decorators: [decorator]
};

export default meta;
