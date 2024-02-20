import React from 'react';
import { render } from '@testing-library/react';

import { ExperimentCollection } from './ExperimentCollection';


describe('ExperimentCollection', () => {
    xit('forwards to a single experiment if it receives a single object', () => {
        const experiment1 = {
            slug: 'some_slug',
            name: 'Some Experiment'
        }
        jest.mock('../../API', () => ({
            useExperimentCollection: () => [false, experiment1]
        }));
        render(<ExperimentCollection match={{params: {slug: 'some_collection'}}}/>)
    });

    xit('shows a dashboard of multiple experiments if it receives an array', () => {
        const experiment1 = {
            slug: 'some_slug',
            name: 'Some Experiment'
        }
        const experiment2 = {
            slug: 'another_slug',
            name: 'Another Experiment'
        }
        jest.mock('../../API', () => ({
            useExperimentCollection: () => [false, {dashboard: [experiment1, experiment2]}]
        }));
        render(<ExperimentCollection match={{params: {slug: 'some_collection'}}}/>)
    });
})