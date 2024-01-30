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
        get: (slug) => "/experiment/" + slug + "/",
        feedback: (slug) => "/experiment/" + slug + "/feedback/",
    },
    participant: {
        current: "/participant/",
        link: "/participant/link/",
        score: "/participant/scores/",
        share: "/participant/share/",
    },
    result: {
        get: (question) => "/result/" + question + "/",
        current: "/result/current_profile",
        score: "/result/score/",
        intermediateScore: "/result/intermediate_score/",
        consent: "/result/consent/"
    },
    session: {
        create: "/session/create/",
        register_playlist: (id) => "/session/" + id + "/register_playlist/",
        next_round: (id) => "/session/" + id + "/next_round/",
        finalize: (id) => "/session/" + id + "/finalize/"
    },
};

export const useExperiment = (slug) =>
    useGet(API_BASE_URL + URLS.experiment.get(slug));

export const useParticipantScores = () =>
    useGet(API_BASE_URL + URLS.participant.score);

export const useParticipantLink = () =>
    useGet(API_BASE_URL + URLS.participant.link);

export const useConsent = (slug) =>
    useGet(API_BASE_URL + URLS.result.get('consent_' + slug));

// Create consent for given experiment
export const createConsent = async ({ experiment, participant }) => {
    try {
        const response = await axios.post(
            API_BASE_URL + URLS.result.consent,
            qs.stringify({
                json_data: JSON.stringify(
                    {
                        key: "consent_" + experiment.slug,
                        value: true,
                    }
                ),
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
export const createSession = async ( {experiment, participant} ) => {
    try {
        const response = await axios.post(
            API_BASE_URL + URLS.session.create,
            qs.stringify({
                experiment_id: experiment.id,
                csrfmiddlewaretoken: participant.csrf_token,
            })
        );
        return response.data;
    } catch (err) {
        console.error(err);
        return null;
    }
};

export const registerPlaylist = async (playlistId, participant, session) => {
    try {
        const response = await axios.post(
            API_BASE_URL + URLS.session.register_playlist(session.id),
            qs.stringify({
                playlist_id: playlistId,
                csrfmiddlewaretoken: participant.csrf_token
            })
        )
        return response.data;
    } catch(err) {
        console.error(err);
        return null;
    }
}

// Create result for given session
export const scoreResult = async ({
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
            API_BASE_URL + URLS.result.score,
            qs.stringify(vars)
        );
        return response.data;
    } catch (err) {
        console.error(err);
        return null;
    }
};

export const scoreIntermediateResult = async ({
    session,
    participant,
    result,
}) => {
    try {
        const vars = {
            session_id: session.id,
            json_data: JSON.stringify(result),
            csrfmiddlewaretoken: participant.csrf_token
        };

        const response = await axios.post(
            API_BASE_URL + URLS.result.intermediateScore,
            qs.stringify(vars)
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

// Tell the backend that the session is finished
export const finalizeSession = async ({ session, participant }) => {
    try {
        const response = await axios.post(
            API_BASE_URL + URLS.session.finalize(session.id),
            qs.stringify({
                csrfmiddlewaretoken: participant.csrf_token,
            })
        );
        return response.data;
    } catch (err) {
        console.error(err);
        return null;
    }
}

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

// Collect user feedback
export const postFeedback = async({ experimentSlug, feedback, participant }) => {
    const endpoint = API_BASE_URL + URLS.experiment.feedback(experimentSlug)
    try {
        const response = await axios.post(
            endpoint,
            qs.stringify({
                feedback,
                csrfmiddlewaretoken: participant.csrf_token,
            })
        );
        return response.data;
    } catch (err) {
        console.error(err);
        return null;
    }
}
