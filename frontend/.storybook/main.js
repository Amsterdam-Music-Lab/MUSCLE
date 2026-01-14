import { join, dirname } from "path";
import { mergeConfig } from 'vite';

/**
 * This function is used to resolve the absolute path of a package.
 * It is needed in projects that use Yarn PnP or are set up within a monorepo.
 */
function getAbsolutePath(value) {
    return dirname(require.resolve(join(value, "package.json")));
}

/** @type { import('@storybook/react-vite').StorybookConfig } */
const config = {
    stories: ["../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],

    addons: [
        getAbsolutePath("@storybook/addon-onboarding"),
        getAbsolutePath("@storybook/addon-links"),
        getAbsolutePath("@storybook/addon-essentials"),
        getAbsolutePath("@chromatic-com/storybook"),
        getAbsolutePath("@storybook/addon-interactions"),
    ],

    framework: {
        name: getAbsolutePath("@storybook/react-vite"),
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
