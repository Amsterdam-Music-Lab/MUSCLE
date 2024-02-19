module.exports = {
    useSessionStore: (fn) => {
        const methods = {
            setSession: jest.fn(),
            session: {id: 1}
        } 
        return fn(methods);
    },
    useParticipantStore: () => {
        return {id: 1}
    },
    useErrorStore: () => {
        return {setError: jest.fn()}
    }
};