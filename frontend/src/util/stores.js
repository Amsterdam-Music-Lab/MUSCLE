import { create } from "zustand";

// Stores
export const createErrorSlice = (set) => ({
    error: null,
    setError: (error) => set(() => ({ error }))
});

export const createParticipantSlice = (set) => ({
    participant: null,
    setParticipant: (participant) => set(() => ({ participant }))
});

export const createSessionSlice = (set) => ({
    session: null,
    setSession: (session) => set(() => ({ session }))
});

export const useBoundStore = create((...args) => ({
    ...createErrorSlice(...args),
    ...createParticipantSlice(...args),
    ...createSessionSlice(...args)
}));

export default useBoundStore;