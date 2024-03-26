import React from 'react';
import { render, screen } from '@testing-library/react';

import ExperimentCollectionAbout from './ExperimentCollectionAbout';

describe('ExperimentCollectionAbout', () => {

    it('shows the about page content', () => {

        const content = '## Hello World!\n\n**Lorem ipsum**';

        render(
            <ExperimentCollectionAbout content={content} />
        );

        expect(screen.getByRole('contentinfo').innerHTML).toContain('Hello World!');
        expect(screen.getByRole('contentinfo').innerHTML).toContain('Lorem ipsum');
    });
})