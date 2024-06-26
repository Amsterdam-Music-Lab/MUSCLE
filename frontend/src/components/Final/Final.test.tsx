import React from 'react';
import { vi, expect, describe, it } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter, Router } from 'react-router-dom';
import { createMemoryHistory } from 'history'
import * as API from '../../API';

import Final from './Final'; // Adjust the import path as necessary

vi.mock('../../util/stores', () => ({
    __esModule: true,
    default: (fn) => {
        const state = {
            setSession: vi.fn(),
            session: 1,
            participant: 'participant-id',
        };

        return fn(state);
    },
    useBoundStore: vi.fn()
}));

vi.mock('../../API', () => ({
    finalizeSession: vi.fn(),
}));

vi.mock('../../API');

vi.mock('../../config', () => {
    return {
        SILENT_MP3: '',
        API_ROOT: '',
        URLS: {
            AMLHome: '/aml',
            profile: '/profile',
        }
    }
});

describe('Final Component', () => {
    it('renders correctly with given props', () => {
        render(
            <BrowserRouter>
                <Final
                    block={{ slug: 'test-experiment' }}
                    participant="participant-id"
                    score={100}
                    final_text="<p>Final Text</p>"
                    rank={1}
                />
            </BrowserRouter>
        );

        expect(document.body.contains(screen.queryByText('Final Text'))).toBe(true);
        expect(document.body.contains(screen.queryByTestId('score'))).toBe(true);
    });

    it('calls onNext prop when button is clicked', async () => {
        const onNextMock = vi.fn();
        render(
            <BrowserRouter>
                <Final
                    button={{ text: 'Next', link: '' }}
                    onNext={onNextMock}
                />
            </BrowserRouter>
        );

        fireEvent.click(screen.getByTestId('button'));
        await waitFor(() => {
            expect(onNextMock).toHaveBeenCalled();
        });
    });

    it('does not render rank and social components when props are not provided', () => {
        render(
            <BrowserRouter>
                <Final
                    experiment={{ slug: 'test-experiment' }}
                    participant="participant-id"
                    score={100}
                    final_text="<p>Final Text</p>"
                />
            </BrowserRouter>
        );

        expect(document.body.contains(screen.queryByTestId('rank'))).toBe(false);
        expect(document.body.contains(screen.queryByTestId('social'))).toBe(false);
    });

    it('navigates to profile page when profile link is clicked', async () => {

        const history = createMemoryHistory();

        const mockActionTexts = {
            all_experiments: 'All Experiments',
            profile: 'Profile',
        };

        render(
            <Router history={history}>
                <Final
                    show_profile_link={true}
                    action_texts={mockActionTexts}
                />
            </Router>
        );

        const profileLink = screen.getByTestId('profile-link');

        expect(document.body.contains(profileLink)).toBe(true);

        expect(history.location.pathname).toBe('/');

        fireEvent.click(profileLink)

        expect(history.location.pathname).toBe('/profile');

    });

    it('calls finalizeSession with correct arguments', () => {

        API.finalizeSession = vi.fn()

        render(
            <BrowserRouter>
                <Final
                    participant="participant-id"
                    session="session-id"
                />
            </BrowserRouter>
        );

        expect(API.finalizeSession).toHaveBeenCalledWith({ session: 1, participant: 'participant-id' });
    });

    it('Uses Link to navigate when button link is relative', () => {
        render(
            <BrowserRouter>
                <Final
                    button={{ text: 'Next', link: '/aml' }}
                />
            </BrowserRouter>
        );

        const el = screen.getByTestId('button-link');
        expect(document.body.contains(el)).toBe(true);
        expect(el.getAttribute('href')).toBe('/redirect/aml');
    });

    it('Uses an anchor tag to navigate when button link is absolute', () => {
        render(
            <BrowserRouter>
                <Final
                    button={{ text: 'Next', link: 'https://example.com' }}
                />
            </BrowserRouter>
        );

        const el = screen.getByTestId('button-link');
        expect(document.body.contains(el)).toBe(true);
        expect(el.getAttribute('href')).toBe('https://example.com');
    });

    it('Calls onNext when there is no button link and the user clicks the button', async () => {
        const onNextMock = vi.fn();
        render(
            <BrowserRouter>
                <Final
                    button={{ text: 'Next' }}
                    onNext={onNextMock}
                />
            </BrowserRouter>
        );

        fireEvent.click(screen.getByTestId('button'));
        await waitFor(() => {
            expect(onNextMock).toHaveBeenCalled();
        });
    });
});
