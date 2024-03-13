//...
import * as Sentry from "@sentry/react";

const SENTRY_DSN = import.meta.env.VITE_SENTRY_DSN;

export const initSentry = () => {

    if (!SENTRY_DSN) {
        console.warn("Sentry DSN not found. Sentry will not be initialized.");
        return;
    }

    return Sentry.init({
        dsn: SENTRY_DSN,
        integrations: [
            new Sentry.BrowserTracing({
                // Set 'tracePropagationTargets' to control for which URLs distributed tracing should be enabled
                tracePropagationTargets: ["localhost", /^https:\/\/yourserver\.io\/api/],
            }),
            new Sentry.Replay(),
        ],
        // Performance Monitoring
        tracesSampleRate: 0.1, // Capture 100% of the transactions
        // Session Replay
        replaysSessionSampleRate: 0.1, // This sets the sample rate at 10%. You may want to change it to 100% while in development and then sample at a lower rate in production.
        replaysOnErrorSampleRate: 1.0, // If you're not already sampling the entire session, change the sample rate to 100% when sampling sessions where errors occur.
    });
}

export default initSentry;
