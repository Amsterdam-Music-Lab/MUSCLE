import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter, Router } from 'react-router-dom';
import { createMemoryHistory } from 'history'

import Final from './Final'; // Adjust the import path as necessary

jest.mock("../../util/stores", () => ({
    useSessionStore: (fn) => {
        const methods = {
            setSession: jest.fn(),
            session: 1
        }
        return fn(methods)
    }
}))

jest.mock('../../API', () => ({
    finalizeSession: jest.fn(),
}));

jest.mock('../../config', () => ({
    URLS: {
        AMLHome: '/aml',
        profile: '/profile',
    },
}));

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

        expect(screen.getByText(/Final Text/i)).toBeInTheDocument();
        expect(screen.getByTestId('score')).toBeInTheDocument(); // Adjust based on how you display points
    });

    it('calls onNext prop when button is clicked', async () => {
        const onNextMock = jest.fn();
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

        expect(screen.queryByText('Rank')).not.toBeInTheDocument();
        expect(screen.queryByText('Social')).not.toBeInTheDocument();
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

        expect(profileLink).toBeInTheDocument();

        expect(history.location.pathname).toBe('/');

        fireEvent.click(profileLink)

        expect(history.location.pathname).toBe('/profile');

    });

    it('calls finalizeSession with correct arguments', () => {
        const { finalizeSession } = require('../../API');
        render(
            <BrowserRouter>
                <Final
                    participant="participant-id"
                    session="session-id"
                />
            </BrowserRouter>
        );

        expect(finalizeSession).toHaveBeenCalledWith({ session: 1, participant: 'participant-id' });
    });
});
