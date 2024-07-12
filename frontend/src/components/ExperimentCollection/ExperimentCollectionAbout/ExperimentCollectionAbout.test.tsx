import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import { it, expect, describe } from 'vitest';

import ExperimentCollectionAbout from './ExperimentCollectionAbout';

describe('ExperimentCollectionAbout', () => {

    it('shows the about page content', () => {

        const content = '## Hello World!\n\n**Lorem ipsum**';

        render(
            <ExperimentCollectionAbout content={content} />,
            { wrapper: Router }
        );

        expect(screen.getByRole('contentinfo').innerHTML).toContain('Hello World!');
        expect(screen.getByRole('contentinfo').innerHTML).toContain('Lorem ipsum');
    });

    it('shows a "Terug" button with a link to the previous page based on a given slug', () => {

        const content = '## Hello World!\n\n**Lorem ipsum**';

        render(
            <ExperimentCollectionAbout content={content} slug="some_slug" />,
            { wrapper: Router }
        )

        expect(screen.getByRole('link').innerHTML).toContain('Terug');
        expect(screen.getByRole('link').getAttribute('href')).toBe('/some_slug');
    });
})
