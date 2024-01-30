import { create } from "zustand";

// Stores
export const useErrorStore = create((set) => ({
    error: null,
    setError: (error) => set((state) => ({error}))
}));

export const useParticipantStore = create((set) => ({
    participant: null,
    setParticipant: (participant) => set((state) => ({participant}))
}));

export const useSessionStore = create((set) => ({
    session: null,
    setSession: (session) => set((state) => ({session}))
}));