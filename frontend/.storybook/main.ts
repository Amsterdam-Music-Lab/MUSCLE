import { mergeConfig } from 'vite';

/** @type { import('@storybook/react-vite').StorybookConfig } */
const config = {
    stories: ["../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],

    addons: [],

    framework: {
        name: "@storybook/react-vite",
        options: {},
    },

    docs: {},

    viteFinal: (config) => {
        return mergeConfig(config, {
            base: "/MUSCLE/storybook/",
            resolve: {
                alias: {
                    '@/': '/src/',
                },
            },
        });
    },

    staticDirs: ["../public"],

    env: {
        VITE_API_ROOT: "http://localhost:8000",
    },

    typescript: {
        reactDocgen: "react-docgen-typescript"
    }
};
export default config;
