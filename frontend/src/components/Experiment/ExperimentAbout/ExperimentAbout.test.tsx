import { render, screen } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import { it, expect, describe } from 'vitest';

import ExperimentAbout from './ExperimentAbout';

const experiment = {
    slug: "some_slug",
    backButtonText: "Terug",
    aboutContent: '## Hello World!\n\n**Lorem ipsum**',
    theme: {
        colorPrimary: "#d843e2", colorSecondary: "#39d7b8"
    }
}

describe('ExperimentAbout', () => {

    it('shows the about page content', () => {
        render(
            <ExperimentAbout {...experiment} />,
            { wrapper: Router }
        );

        expect(screen.getByRole('contentinfo').innerHTML).toContain('Hello World!');
        expect(screen.getByRole('contentinfo').innerHTML).toContain('Lorem ipsum');
    });

    it('shows a "Terug" button with a link to the previous page based on a given slug', () => {

        render(
            <ExperimentAbout {...experiment} />,
            { wrapper: Router }
        )

        expect(screen.getByRole('link').innerHTML).toContain('Terug');
        expect(screen.getByRole('link').getAttribute('href')).toBe('/some_slug');
    });
})
