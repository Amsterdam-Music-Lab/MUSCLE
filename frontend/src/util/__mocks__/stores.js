module.exports = {
    useSessionStore: (fn) => {
        const methods = {
            setSession: jest.fn(),
            session: 1
        } 
        return fn(methods);
    },
    useParticipantStore: () => {
        return {participant: 1}
    },
    useErrorStore: () => {
        return {setError: jest.fn()}
    }
};