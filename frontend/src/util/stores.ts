import { create } from "zustand";

import IParticipant from "@/types/Participant";
import ISession from "@/types/Session";
import ITheme from "@/types/Theme";

const createErrorSlice = (set) => ({
    error: null,
    setError: (error: string) => set(() => ({ error }))
});

const createParticipantSlice = (set) => ({
    participant: null,
    setParticipant: (participant: IParticipant) => set(() => ({ participant }))
});

const createSessionSlice = (set) => ({
    session: null,
    setSession: (session: ISession) => set(() => ({ session }))
});

const createThemeSlice = (set) => ({
    theme: null,
    setTheme: (theme: ITheme) => set(() => ({ theme })),
});

export const useBoundStore = create((...args) => ({
    ...createErrorSlice(...args),
    ...createParticipantSlice(...args),
    ...createSessionSlice(...args),
    ...createThemeSlice(...args),
}));

export default useBoundStore;