import * as Sentry from '@sentry/react';
import { StateCreator, create } from "zustand";

import IParticipant from "@/types/Participant";
import ISession from "@/types/Session";
import ITheme from "@/types/Theme";
import IBlock from "@/types/Block";
import { Action, Round } from '@/types/Round';

interface BlockSlice {
    block?: IBlock;
    setBlock: (block: IBlock) => void;
}

const createBlockSlice: StateCreator<BlockSlice> = (set) => ({
    block: undefined,
    setBlock: (block) => set(() => ({ block })),
});

interface StructuredData {
    "@context": string;
    "@type": string;
    url: string;
    logo: string;
    name: string;
    description: string;
}

interface HeadData {
    title: string;
    description: string;
    image: string;
    url: string;
    structuredData: Partial<StructuredData>;
}

export interface DocumentHeadSlice {
    headData: HeadData;
    setHeadData: (headData: HeadData) => void;
    patchHeadData: (headData: Partial<HeadData>) => void;
    resetHeadData: () => void;
}

const createDocumentHeadSlice: StateCreator<DocumentHeadSlice> = (set) => ({
    headData: {
        title: "",
        description: "",
        image: "",
        url: "",
        structuredData: {
            "@context": "http://schema.org",
            "@type": "Organization",
            url: import.meta.env.VITE_OG_URL ?? "",
            logo: import.meta.env.VITE_OG_IMAGE ?? "",
            name: import.meta.env.VITE_OG_TITLE ?? "",
            description: import.meta.env.VITE_OG_DESCRIPTION ?? "",
        }
    },
    setHeadData: (headData) => set(() => ({ headData })),
    patchHeadData: (headData) => set((state) => ({ headData: { ...state.headData, ...headData } })),
    resetHeadData: () => set(() => ({
        headData: {
            title: import.meta.env.VITE_OG_TITLE ?? "",
            description: import.meta.env.VITE_OG_DESCRIPTION ?? "",
            image: import.meta.env.VITE_OG_IMAGE ?? "",
            url: import.meta.env.VITE_OG_URL ?? "",
        }
    }))
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

interface ActionSlice {
    currentAction: Action | null;
    setCurrentAction: (action: Action) => void;
}

const createActionSlice: StateCreator<ActionSlice> = (set, get) => ({
    setCurrentAction: (action: Action) => set(() => ({ currentAction: action })),
    currentAction: null,
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
    resetTheme: () => void;
}

const createThemeSlice: StateCreator<ThemeSlice> = (set) => ({
    theme: null,
    setTheme: (theme: ITheme) => set(() => ({ theme })),
    resetTheme: () => set(() => ({ theme: null })),
});

export const useBoundStore = create<BlockSlice & DocumentHeadSlice & ErrorSlice & ParticipantSlice & ActionSlice & SessionSlice & ThemeSlice>((...args) => ({
    ...createBlockSlice(...args),
    ...createDocumentHeadSlice(...args),
    ...createErrorSlice(...args),
    ...createParticipantSlice(...args),
    ...createActionSlice(...args),
    ...createSessionSlice(...args),
    ...createThemeSlice(...args),
}));

export default useBoundStore;
