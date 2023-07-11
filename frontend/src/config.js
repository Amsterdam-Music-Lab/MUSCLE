// Load experiment slug from hash, or default to env experiment slug
export const EXPERIMENT_SLUG =
    document.location.hash.indexOf("slug=") > -1
        ? document.location.hash.split("slug=")[1]
        : process.env.REACT_APP_EXPERIMENT_SLUG;


// Base url the API
// Make sure your app url is set in the CORS_ORIGIN_WHITELIST in
// the API's base_settings.py

export const API_ROOT = process.env.REACT_APP_API_ROOT;
export const API_BASE_URL = API_ROOT;

// Media
export const MEDIA_ROOT = API_ROOT;
export const SILENT_MP3 = "/audio/silent.mp3";

// Logo
export const LOGO_URL = process.env.REACT_APP_LOGO_URL || '/images/logo-white.svg';
export const LOGO_TITLE = process.env.REACT_APP_HTML_PAGE_TITLE || 'Amsterdam Music Lab';

// Urls used by app
export const URLS = {
    home: "/",
    about: "/about",
    profile: "/profile",
    storeProfile: "/profile/store",
    experiment: "/:slug",
    reloadParticipant: "/participant/reload/:id/:hash",
    AMLHome:
        process.env.REACT_APP_AML_HOME || "https://www.amsterdammusiclab.nl",

    // share
    shareFacebook:
        "https://www.facebook.com/sharer/sharer.php?u=https://app.amsterdammusiclab.nl--SLUG--",
    shareTwitter:
        "https://twitter.com/intent/tweet?text=" +
        encodeURIComponent(
            "I scored --SCORE-- points on #amsterdammusiclab--HASHTAG--#citizenscience https://app.amsterdammusiclab.nl--SLUG--"
        ),
};
