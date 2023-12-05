//...
import * as Sentry from "@sentry/react";


export const initSentry = () =>
    Sentry.init({
        dsn: "https://21d71c12f155fb5aae96a480ed35c473@o4506343330021376.ingest.sentry.io/4506343351320576",
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

export default initSentry;
