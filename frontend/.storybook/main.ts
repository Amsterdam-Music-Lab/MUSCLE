import type { StorybookConfig } from '@storybook/react-vite';
import { mergeConfig } from 'vite';

const config: StorybookConfig = {
  stories: ["../src/**/*.mdx", "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-onboarding",
    "@storybook/addon-interactions",
  ],
  core: {
    builder: '@storybook/builder-vite',
  },
  docs: {
    autodocs: "tag",
  },
  viteFinal: (config) => {
    return mergeConfig(config, {
      esbuild: {
        loader: 'jsx',
      },
      resolve: {
        alias: {
          '@/': '/src/',
        },
      },
    });
  },
  framework: {
    name: "@storybook/react-vite",
    options: { },
  },
  staticDirs: ["../public"],
  env: {
    VITE_API_ROOT: "http://localhost:8000",
  },
};

export default config;
