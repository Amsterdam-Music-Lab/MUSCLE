import { API_BASE_URL } from "@/config";
import useGet, { Params } from "./util/useGet";
import axios from "axios";
import qs from "qs";
import IBlock from "@/types/Block";
import IExperiment from "@/types/Experiment";
import Participant, { ParticipantLink } from "./types/Participant";
import Session from "./types/Session";
import Experiment from "@/types/Experiment";
import { RoundResponse } from "./types/Round";

// API handles the calls to the Hooked-server api

// Include creditials (cookie) in each call
axios.defaults.withCredentials = true;

// API endpoints
export const URLS = {
    block: {
        get: (slug: string) => "/experiment/block/" + slug + "/",
        feedback: (slug: string) => "/experiment/block/" + slug + "/feedback/",
    },
    experiment: {
        get: (slug: string) => `/experiment/${slug}/`
    },
    participant: {
        current: "/participant/",
        link: "/participant/link/",
        score: "/participant/scores/",
        share: "/participant/share/",
    },
    result: {
        get: (question: string) => "/result/" + question + "/",
        current: "/result/current_profile",
        score: "/result/score/",
        intermediateScore: "/result/intermediate_score/",
        consent: "/result/consent/"
    },
    session: {
        create: "/session/create/",
        next_round: (id: string) => "/session/" + id + "/next_round/",
        finalize: (id: string) => "/session/" + id + "/finalize/"
    },
    theme: {
        get: (id: string) => `/theme/${id}`,
    }
};

export const useBlock = (slug: string) =>
    useGet<IBlock>(API_BASE_URL + URLS.block.get(slug));

export const useExperiment = (slug: string) => {
    return useGet<Experiment>(API_BASE_URL + URLS.experiment.get(slug));
}

export const useParticipantScores = <T>() =>
    useGet<T>(API_BASE_URL + URLS.participant.score);

export const useParticipantLink = () =>
    useGet<ParticipantLink>(API_BASE_URL + URLS.participant.link);

type ConsentResponse = boolean | null;

export const useConsent = (slug: string) =>
    useGet<ConsentResponse>(API_BASE_URL + URLS.result.get('consent_' + slug));

interface CreateConsentParams {
    experiment: IExperiment;
    participant: Pick<Participant, 'csrf_token'>;
}

/** Create consent for given experiment */
export const createConsent = async ({ experiment, participant }: CreateConsentParams) => {
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

interface ScoreResultParams {
    session: Session;
    participant: Participant;
    result: unknown;
    section?: { id: number };
}

interface ScoreResultPayload {
    session_id: number;
    json_data: string;
    csrfmiddlewaretoken: string;
    section_id?: number;
}

// Create result for given session
export const scoreResult = async ({
    session,
    section,
    participant,
    result,
}: ScoreResultParams) => {
    try {
        const vars: ScoreResultPayload = {
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

interface ScoreIntermediateResultParams {
    session: Session;
    participant: Participant;
    result: unknown;
}

interface ScoreIntermediateResultResponse {
    score: number;
}

export const scoreIntermediateResult = async ({
    session,
    participant,
    result,
}: ScoreIntermediateResultParams): Promise<ScoreIntermediateResultResponse | null> => {
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

interface GetNextRoundParams {
    session: Session;
}


// Get next_round from server
export const getNextRound = async ({ session }: GetNextRoundParams): Promise<RoundResponse | null> => {

    const sessionId = session.id.toString();

    try {
        const response = await axios.get(API_BASE_URL + URLS.session.next_round(sessionId));
        return response.data;
    } catch (err) {
        console.error(err);
        return null;
    }
};

interface FinalizeSessionParams {
    session: Session;
    participant: Participant;
}

// Tell the backend that the session is finished
export const finalizeSession = async ({ session, participant }: FinalizeSessionParams) => {

    const sessionId = session.id.toString();

    try {
        const response = await axios.post(
            API_BASE_URL + URLS.session.finalize(sessionId),
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

interface ShareParticipantParams {
    email: string;
    participant: Participant;
}

// Share participant
export const shareParticipant = async ({ email, participant }: ShareParticipantParams) => {
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

interface PostFeedbackParams {
    blockSlug: string;
    feedback: string;
    participant: Participant;
}

// Collect user feedback
export const postFeedback = async ({ blockSlug, feedback, participant }: PostFeedbackParams) => {
    const endpoint = API_BASE_URL + URLS.block.feedback(blockSlug)
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
