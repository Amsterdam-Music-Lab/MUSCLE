import { create } from "zustand";

const createErrorSlice = (set) => ({
    error: null,
    setError: (error) => set(() => ({ error }))
});

const createParticipantSlice = (set) => ({
    participant: null,
    setParticipant: (participant) => set(() => ({ participant }))
});

const createSessionSlice = (set) => ({
    session: null,
    setSession: (session) => set(() => ({ session }))
});

const createThemeSlice = (set) => ({
    theme: null,
    setTheme: (theme) => set(() => ({ theme })),
});

export const useBoundStore = create((...args) => ({
    ...createErrorSlice(...args),
    ...createParticipantSlice(...args),
    ...createSessionSlice(...args),
    ...createThemeSlice(...args),
}));

export default useBoundStore;