// Load experiment slug from hash, or default to env experiment slug
export const EXPERIMENT_SLUG =
    document.location.hash.indexOf("slug=") > -1
        ? document.location.hash.split("slug=")[1]
        : process.env.REACT_APP_EXPERIMENT_SLUG;

// Base url the API
// Make sure your app url is set in the CORS_ORIGIN_WHITELIST in
// the API's base_settings.py

export const API_ROOT = process.env.REACT_APP_API_ROOT;
export const API_BASE_URL = API_ROOT + '/experiment';

// Media
export const MEDIA_ROOT = API_ROOT;
export const SILENT_MP3 = MEDIA_ROOT + "/static/audio/silent.mp3";

// Urls used by app
export const URLS = {
    home: "/",
    about: "/about",
    profile: "/profile",
    storeProfile: "/profile/store",
    experiment: "/experiment/:slug",
    reloadParticipant: "/participant/reload/:id/:hash",
    AMLHome:
        process.env.REACT_APP_AML_HOME || "https://www.amsterdammusiclab.nl",

    // share
    shareFacebook:
        "https://www.facebook.com/sharer/sharer.php?u=https://app.amsterdammusiclab.nl",
    shareTwitter:
        "https://twitter.com/intent/tweet?text=" +
        encodeURIComponent(
            "I scored --SCORE-- points on Amsterdam Music Lab - #amsterdammusiclab #citizenscience https://app.amsterdammusiclab.nl"
        ),
};
