// Load experiment IDENTIFIER from hash, or default to env experiment identifier
export const EXPERIMENT_identifier: string =
    document.location.hash.indexOf("identifier=") > -1
        ? document.location.hash.split("identifier=")[1]
        : import.meta.env.VITE_EXPERIMENT_IDENTIFIER;


// Base url the API
// Make sure your app url is set in the CORS_ORIGIN_WHITELIST in
// the API's base_settings.py

export const API_ROOT: string = import.meta.env.VITE_API_ROOT;
export const API_BASE_URL = API_ROOT;

// Media
export const SILENT_MP3 = "/audio/silent.mp3";

// Logo
export const LOGO_URL: string = import.meta.env.VITE_LOGO_URL || '/images/logo-white.svg';
export const LOGO_TITLE: string = import.meta.env.VITE_HTML_PAGE_TITLE || 'Amsterdam Music Lab';

// Background
export const BACKGROUND_URL = import.meta.env.VITE_BACKGROUND_URL || '/images/background.jpg'

// Urls used by app
export const URLS = {
    home: "/",
    about: "/about",
    profile: "/profile",
    storeProfile: "/profile/store",
    block: "/block/:identifier",
    experimentAbout: "/:identifier/about",
    experiment: "/:identifier/*",
    internalRedirect: "/redirect/*",
    reloadParticipant: "/participant/reload/:id/:hash",
    theme: "/theme/:id",
    AMLHome:
        import.meta.env.VITE_AML_HOME as string || "https://www.amsterdammusiclab.nl",
};
