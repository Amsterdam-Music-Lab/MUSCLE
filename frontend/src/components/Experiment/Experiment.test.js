import React from 'react';
import { MemoryRouter } from 'react-router-dom/cjs/react-router-dom';
import { render, screen } from '@testing-library/react';

import Experiment from './Experiment';

jest.mock("../../util/stores", () => ({
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
}));

jest.mock("../../API", () => ({
    useExperiment: () => {return [{id: 24, slug: 'test', name: 'Test', next_round: [
        {view: 'EXPLAINER'}
    ]}, false]},
    createSession: () => Promise.resolve({data: {session: 1}})
}));

describe('Experiment Component', () => {

    it('renders with given props', () => {

        render(
            <MemoryRouter>
                <Experiment match={ {params: {slug: 'test'}} }/>
            </MemoryRouter>
        );
        expect(screen.getByTestId('experiment-wrapper').toBeInTheDocument());
    })



});