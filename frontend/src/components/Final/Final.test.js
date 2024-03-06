import React from 'react';
import { vi } from 'vitest';
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
    finalizeSession: jest.fn(),
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
                    experiment={{ slug: 'test-experiment' }}
                    participant="participant-id"
                    score={100}
                    final_text="<p>Final Text</p>"
                    rank={1}
                />
            </BrowserRouter>
        );

        expect(screen.queryByText(/Final Text/i)).to.exist;
        expect(screen.queryByTestId('score')).to.exist;
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

        fireEvent.click(screen.getByText('Next'));
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

        expect(screen.queryByText('Rank')).to.not.exist;
        expect(screen.queryByText('Social')).to.not.exist;
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

        expect(profileLink).to.exist;

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
});
