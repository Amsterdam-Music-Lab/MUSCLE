import { initialize, mswLoader } from 'msw-storybook-addon'
import "../public/vendor/bootstrap/bootstrap.min.css";
import "../src/index.scss";
import { initAudioListener } from "../src/util/audio";
import { initWebAudioListener } from "../src/util/webAudio";
import { ThemeProvider } from "@/theme/ThemeProvider";
import { themes, type ThemeName } from '@/theme/themes';

// Init audio listener
initAudioListener();
initWebAudioListener();

// Initialize MSW
initialize({
    serviceWorker: {
        url: './mockServiceWorker.js',
    },

    // Silence unhandled request warnings
    onUnhandledRequest: 'bypass',
});

// Global decorator to provide the theme context
const withThemeProvider = (Story, context) => {
    const themeName = context.globals.theme as ThemeName;
    const theme = themes[themeName] ?? themes.default;

    return (
        <ThemeProvider useTheme={theme}>
            <div className="theme-root">
                <Story />
            </div>
        </ThemeProvider>
    );
}
  
/** @type { import('@storybook/react').Preview } */
const preview = {
    parameters: {
        controls: {
            matchers: {
                color: /(background|color)$/i,
                date: /Date$/i,
            },
        },
    },

    // Provide the MSW addon loader globally
    loaders: [mswLoader],

    // Allow selecting the theme in the Storybook UI
    globalTypes: {
        theme: {
            name: 'Theme',
            description: 'Global theme for components',
            defaultValue: 'mcgLight',
            toolbar: {
                icon: 'paintbrush',
                items: Object.keys(themes),
                showName: true,
            },
        },
    },
    decorators: [withThemeProvider],
};



export default preview;
