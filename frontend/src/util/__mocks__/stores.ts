import { vi } from 'vitest';

module.exports = {
    useBoundStore: () => {
        return {
            setError: vi.fn(),
            setParticipant: vi.fn(),
            setSession: vi.fn(),
            participant: { id: 1 },
            session: { id: 1 }
        }
    }
};