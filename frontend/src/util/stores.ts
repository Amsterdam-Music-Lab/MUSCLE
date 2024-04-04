import * as Sentry from '@sentry/react';
import { StateCreator, create } from "zustand";

import IParticipant from "@/types/Participant";
import ISession from "@/types/Session";
import ITheme from "@/types/Theme";

interface DocumentHeadSlice {
    pageTitle: string;
    setPageTitle: (title: string) => void;
    pageDescription: string;
    setPageDescription: (description: string) => void;
    pageImage: string;
    setPageImage: (image: string) => void;
    pageUrl: string;
    setPageUrl: (url: string) => void;
}

const createDocumentHeadSlice: StateCreator<DocumentHeadSlice> = (set) => ({
    pageTitle: "",
    setPageTitle: (pageTitle) => set(() => ({ pageTitle })),
    pageDescription: "",
    setPageDescription: (pageDescription) => set(() => ({ pageDescription })),
    pageImage: "",
    setPageImage: (pageImage) => set(() => ({ pageImage })),
    pageUrl: "",
    setPageUrl: (pageUrl) => set(() => ({ pageUrl })),
});

interface ErrorSlice {
    error: string | null;
    setError: (message: string, errorToCapture?: Error) => void;
}

const createErrorSlice: StateCreator<ErrorSlice> = (set) => ({
    error: null,
    setError: (message, errorToCapture) => {
        set(() => ({ error: message }));
        if (errorToCapture) {
            Sentry.captureException(errorToCapture);
        }
    }
});

interface ParticipantSlice {
    participant: IParticipant | null;
    participantLoading: boolean;
    setParticipant: (participant: IParticipant) => void;
    setParticipantLoading: (participantLoading: boolean) => void;
}

const createParticipantSlice: StateCreator<ParticipantSlice> = (set) => ({
    participant: null,
    participantLoading: true,
    setParticipant: (participant: IParticipant) => set(() => ({ participant })),
    setParticipantLoading: (participantLoading: boolean) => set(() => ({ participantLoading }))
});

interface SessionSlice {
    session: ISession | null;
    setSession: (session: ISession) => void;
}

const createSessionSlice: StateCreator<SessionSlice> = (set) => ({
    session: null,
    setSession: (session: ISession) => set(() => ({ session })),
});

interface ThemeSlice {
    theme: ITheme | null;
    setTheme: (theme: ITheme) => void;
}

const createThemeSlice: StateCreator<ThemeSlice> = (set) => ({
    theme: null,
    setTheme: (theme: ITheme) => set(() => ({ theme })),
});

export const useBoundStore = create<ErrorSlice & ParticipantSlice & SessionSlice & ThemeSlice>((...args) => ({
    ...createDocumentHeadSlice(...args),
    ...createErrorSlice(...args),
    ...createParticipantSlice(...args),
    ...createSessionSlice(...args),
    ...createThemeSlice(...args),
}));

export default useBoundStore;