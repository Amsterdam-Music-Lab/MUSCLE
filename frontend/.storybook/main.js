/** @type { import('@storybook/react-webpack5').StorybookConfig } */
const config = {
    stories: ["../src/**/*.mdx", "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
    addons: [
        "@storybook/addon-links",
        "@storybook/addon-essentials",
        "@storybook/preset-create-react-app",
        "@storybook/addon-onboarding",
        "@storybook/addon-interactions",
    ],
    framework: {
        name: "@storybook/react-webpack5",
        options: {},
    },
    docs: {
        autodocs: "tag",
    },
    staticDirs: ["../public"],
    env: {
        REACT_APP_API_ROOT: "http://localhost:8000",
    },
    webpackFinal: async (config) => {
        (config.resolve.alias = {
            ...config.resolve.alias,
            util: require("path").resolve(__dirname, "../src/util"),
        }),
            (config.resolve.alias = {
                ...config.resolve.alias,
                components: require("path").resolve(
                    __dirname,
                    "../src/components"
                ),
            });
        return config;
    }
};

export default config;
