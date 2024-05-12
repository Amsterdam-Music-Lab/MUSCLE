import { create, StateCreator } from "zustand";
import * as Sentry from '@sentry/react';
import { Participant } from "@/types/Participant";

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
    participant: Participant | null;
    participantLoading: boolean;
    setParticipant: (participant: Participant) => void;
    setParticipantLoading: (participantLoading: boolean) => void;
}

const createParticipantSlice: StateCreator<ParticipantSlice> = (set) => ({
    participant: null,
    participantLoading: true,
    setParticipant: (participant) => set(() => ({ participant })),
    setParticipantLoading: (participantLoading) => set(() => ({ participantLoading }))
});

interface SessionSlice {
    session: string | null;
    setSession: (session: string) => void;
}

const createSessionSlice: StateCreator<SessionSlice> = (set) => ({
    session: null,
    setSession: (session) => set(() => ({ session }))
});

interface ThemeSlice {
    theme: string | null;
    setTheme: (theme: string) => void;
}

const createThemeSlice: StateCreator<ThemeSlice> = (set) => ({
    theme: null,
    setTheme: (theme) => set(() => ({ theme })),
});

export const useBoundStore = create<ErrorSlice & ParticipantSlice & SessionSlice & ThemeSlice>((...args) => ({
    ...createErrorSlice(...args),
    ...createParticipantSlice(...args),
    ...createSessionSlice(...args),
    ...createThemeSlice(...args),
}));

export default useBoundStore;