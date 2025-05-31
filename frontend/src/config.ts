// Load experiment slug from hash, or default to env experiment slug
export const EXPERIMENT_SLUG: string =
  document.location.hash.indexOf("slug=") > -1
    ? document.location.hash.split("slug=")[1]
    : import.meta.env.VITE_EXPERIMENT_SLUG;

// Base url the API
// Make sure your app url is set in the CORS_ORIGIN_WHITELIST in
// the API's base_settings.py

export const API_ROOT: string = import.meta.env.VITE_API_ROOT;
export const API_BASE_URL = API_ROOT;

// Media
export const SILENT_MP3 = "/audio/silent.mp3";

// Logo
export const LOGO_URL: string =
  import.meta.env.VITE_LOGO_URL || "/images/logo-white.svg";
export const LOGO_TITLE: string =
  import.meta.env.VITE_HTML_PAGE_TITLE || "Amsterdam Music Lab";

// Background
export const BACKGROUND_URL =
  import.meta.env.VITE_BACKGROUND_URL || "/images/background.jpg";

type QueryParams = Record<string, string | number | boolean | undefined | null>;

export function toQueryParams(params: QueryParams): string {
  const esc = encodeURIComponent;
  const query = Object.entries(params)
    .filter(([_, v]) => v !== undefined && v !== null)
    .map(([k, v]) => `${esc(k)}=${esc(String(v))}`)
    .join("&");
  return query ? `?${query}` : "";
}

function path(path: string, params?: QueryParams) {
  return params ? `${path}${toQueryParams(params)}` : path;
}

const AMLHome = "https://www.amsterdammusiclab.nl";

export const routes = {
  externalHome: (p?: QueryParams) =>
    path((import.meta.env.VITE_AML_HOME as string) || AMLHome, p),
  home: (p?: QueryParams) => path("/", p),
  about: (p?: QueryParams) => path("/about", p),
  profile: (p?: QueryParams) => path("/profile", p),
  storeProfile: (p?: QueryParams) => path("/profile/store", p),
  block: (slug: string, p?: QueryParams) => path(`/block/${slug}`, p),
  experiment: (slug: string, p?: QueryParams) => path(`/${slug}`, p),
  experimentAbout: (slug: string, p?: QueryParams) => path(`/${slug}/about`, p),
  noconsent: (slug: string, p?: QueryParams) => path(`/${slug}/noconsent`, p),
  internalRedirect: (p?: QueryParams) => path("/redirect/*", p),
  reloadParticipant: (id: string, hash: string, p?: QueryParams) =>
    path(`/participant/reload/${id}/${hash}`, p),
  theme: (id: string, p?: QueryParams) => path(`theme/${id}`, p),
};
