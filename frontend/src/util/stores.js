import { create } from "zustand";

// Stores
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

export const useBoundStore = create((...args) => ({
    ...createErrorSlice(...args),
    ...createParticipantSlice(...args),
    ...createSessionSlice(...args)
}));

export default useBoundStore;