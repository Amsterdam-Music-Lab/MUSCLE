module.exports = {
    useBoundStore: () => {
        return {
            setError: jest.fn(),
            setParticipant: jest.fn(),
            setSession: jest.fn(),
            participant: { id: 1 },
            session: { id: 1 }
        }
    }
};