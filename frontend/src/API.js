import { API_BASE_URL } from "./config";
import useGet from "./util/useGet";
import axios from "axios";
import qs from "qs";

// API handles the calls to the Hooked-server api

// Include creditials (cookie) in each call
axios.defaults.withCredentials = true;

// API endpoints
export const URLS = {
    experiment: {
        get: (slug) => "/id/" + slug + "/",
        consent: (slug) => "/profile/consent_" + slug + "/",
    },
    participant: {
        current: "/participant/",
        link: "/participant/link/",
        score: "/participant/scores/",
        share: "/participant/share/",
    },
    profile: {
        get: (question) => "/profile/" + question + "/",
        current: "/profile/",
        create: "/profile/create/",
    },
    session: {
        create: "/session/create/",
        result: "/session/result/",
        next_round: (id) => "/session/" + id + "/next_round/",
    },
};

export const useExperiment = (slug) =>
    useGet(API_BASE_URL + URLS.experiment.get(slug));

export const useParticipant = () =>
    useGet(API_BASE_URL + URLS.participant.current);

export const useParticipantScores = () =>
    useGet(API_BASE_URL + URLS.participant.score);

export const useParticipantLink = () =>
    useGet(API_BASE_URL + URLS.participant.link);

export const useConsent = (slug) =>
    useGet(API_BASE_URL + URLS.experiment.consent(slug));

// Create consent for given experiment
export const createConsent = async ({ experiment, participant }) => {
    try {
        const response = await axios.post(
            API_BASE_URL + URLS.profile.create,
            qs.stringify({
                json_data: JSON.stringify({result: {form: [
                    {
                        question: "consent_" + experiment.slug,
                        value: true,
                    }
                ]}}),
                csrfmiddlewaretoken: participant.csrf_token,
            }),
        );
        return response.data;
    } catch (err) {
        console.error(err);
        return null;
    }
};

// Create a new session for given experiment
export const createSession = async ({ experiment, participant, playlist }) => {
    try {
        const response = await axios.post(
            API_BASE_URL + URLS.session.create,
            qs.stringify({
                experiment_id: experiment.id,
                playlist_id: playlist,
                json_data: "",
                csrfmiddlewaretoken: participant.csrf_token,
            })
        );
        return response.data;
    } catch (err) {
        console.error(err);
        return null;
    }
};

// Create result for given session
export const createResult = async ({
    session,
    section,
    participant,
    result,
}) => {
    try {
        const vars = {
            session_id: session.id,
            json_data: JSON.stringify(result),
            csrfmiddlewaretoken: participant.csrf_token,
        };
        // optional section_id
        if (section) {
            vars["section_id"] = section.id;
        }

        const response = await axios.post(
            API_BASE_URL + URLS.session.result,
            qs.stringify(vars)
        );
        return response.data;
    } catch (err) {
        console.error(err);
        return null;
    }
};

// Store Profile question/answer
export const createProfile = async ({
    result,
    session,
    participant,
}) => {
    try {
        const response = await axios.post(
            API_BASE_URL + URLS.profile.create,
            qs.stringify({
                json_data: JSON.stringify(result),
                session_id: session,
                csrfmiddlewaretoken: participant.csrf_token,
            })
        );
        return response.data;
    } catch (err) {
        console.error(err);
        return null;
    }
};

// Get next_round from server
export const getNextRound = async ({ session }) => {
    try {
        const response = await axios.get( API_BASE_URL + URLS.session.next_round(session.id));
        return response.data;
    } catch (err) {
        console.error(err);
        return null;
    }
};

// Share participant
export const shareParticipant = async ({ email, participant }) => {
    try {
        const response = await axios.post(
            API_BASE_URL + URLS.participant.share,
            qs.stringify({
                email,
                csrfmiddlewaretoken: participant.csrf_token,
            })
        );
        return response.data;
    } catch (err) {
        console.error(err);
        return null;
    }
};
