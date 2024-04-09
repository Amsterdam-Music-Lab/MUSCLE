// Load experiment slug from hash, or default to env experiment slug
export const EXPERIMENT_SLUG =
    document.location.hash.indexOf("slug=") > -1
        ? document.location.hash.split("slug=")[1]
        : import.meta.env.VITE_EXPERIMENT_SLUG;


// Base url the API
// Make sure your app url is set in the CORS_ORIGIN_WHITELIST in
// the API's base_settings.py

export const API_ROOT = import.meta.env.VITE_API_ROOT;
export const API_BASE_URL = API_ROOT;

// Media
export const MEDIA_ROOT = API_ROOT;
export const SILENT_MP3 = "/audio/silent.mp3";

// Logo
export const LOGO_URL = import.meta.env.VITE_LOGO_URL || '/images/logo-white.svg';
export const LOGO_TITLE = import.meta.env.VITE_HTML_PAGE_TITLE || 'Amsterdam Music Lab';

// Background
export const BACKGROUND_URL = import.meta.env.VITE_BACKGROUND_URL || '/images/background.jpg'

// Urls used by app
export const URLS = {
    home: "/",
    about: "/about",
    profile: "/profile",
    storeProfile: "/profile/store",
    experiment: "/:slug",
    experimentCollectionAbout: "/collection/:slug/about",
    experimentCollection: "/collection/:slug",
    reloadParticipant: "/participant/reload/:id/:hash",
    AMLHome:
        import.meta.env.VITE_AML_HOME || "https://www.amsterdammusiclab.nl",
};
