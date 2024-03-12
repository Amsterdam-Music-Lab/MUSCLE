import React from 'react';
import { fireEvent, getByText, render, screen, waitFor } from '@testing-library/react';
import mockAxios from "jest-mock-axios";

import MatchingPairs, { SCORE_FEEDBACK_DISPLAY } from './MatchingPairs';

jest.mock('../../util/stores', () => ({
    __esModule: true,
    default: (fn) => {
        const state = {
            session: 1,
            participant: 'participant-id',
            setError: jest.fn()
        };
        
        return fn(state);
    },
    useBoundStore: jest.fn()
}));

describe('MatchingPairs Component', () => {
    beforeEach(() => {
        jest.resetAllMocks();
    });
    
    const mockSections = [
        { id: 1, content: 'Card 1', url: '/cat-01.jpg', inactive: false, turned: false, noevents: false, seen: false, group: 1 },
        { id: 2, content: 'Card 2', url: '/cat-02.jpg', inactive: false, turned: false, noevents: false, seen: false, group: 2 },
        { id: 3, content: 'Card 1', url: '/cat-01.jpg', inactive: false, turned: false, noevents: false, seen: false, group: 1 },
        { id: 4, content: 'Card 2', url: '/cat-02.jpg', inactive: false, turned: false, noevents: false, seen: false, group: 2 },
    ];

    const baseProps = {
        playSection: jest.fn(),
        playerIndex: 0,
        finishedPlaying: jest.fn(),
        onFinish: jest.fn(),
        stopAudioAfter: 4.0,
        showAnimation: false,
    };

    it('renders correctly', () => {
        const { getByText } = render(<MatchingPairs sections={mockSections} setPlayerIndex={jest.fn()} />);
        expect(getByText('Pick a card')).toBeInTheDocument();
    });

    it('flips a card when clicked', async () => {
        render(<MatchingPairs {...baseProps} sections={mockSections} setPlayerIndex={jest.fn()} />);
        const cards = screen.getAllByRole('button'); // Assuming each card is a button, adjust if necessary

        fireEvent.click(cards[0]);

        await waitFor(() => expect(cards[0]).toHaveClass('turned'));
    });

    it('updates score after a match', async () => {
    mockAxios.post.mockResolvedValueOnce({data: {score: 10}});
    const { getByText } = render(<MatchingPairs {...baseProps} sections={mockSections} setPlayerIndex={jest.fn()} />);
    const cards = screen.getAllByRole('button');

    fireEvent.click(cards[0]);
    fireEvent.click(cards[2]);

    await waitFor( () => expect(getByText('Score: 110')).toBeInTheDocument());
    });

    xit('has a blocking overlay in-between turns', async () => {
        mockAxios.post.mockResolvedValueOnce({data: {score: 0}});
        render(<MatchingPairs {...baseProps} sections={mockSections} setPlayerIndex={jest.fn()} />);
        const cards = screen.getAllByRole('button');

        await waitFor(() => expect(screen.getByTestId('overlay')).toHaveStyle('display: none'));

        fireEvent.click(cards[0]);
        fireEvent.click(cards[1]);

        await waitFor(() => expect(screen.getByTestId('overlay')).toHaveStyle('display: block'));
    });

    xit('calls scoreIntermediateResult after each turn', async() => {
        const api = require('../../API');
        const spy = jest.spyOn(api, 'scoreIntermediateResult');
        mockAxios.post.mockResolvedValueOnce({data: {score: 10}});
        render(<MatchingPairs {...baseProps} sections={mockSections} setPlayerIndex={jest.fn()} />);
        const cards = screen.getAllByTestId('play-card');

        fireEvent.click(cards[0]);
        fireEvent.click(cards[2]);
        fireEvent.click(screen.getByTestId('overlay'));

        await waitFor(() => screen.getByText('Pick a card'));
        expect(spy).toHaveBeenCalled();
    })


    xit('ends the game when all pairs are matched', async () => {
        mockAxios.post.mockResolvedValue({data: {score: 10}});
        const submitResult = jest.fn();
        render(
            <MatchingPairs {...baseProps} sections={mockSections} setPlayerIndex={jest.fn()} submitResult={submitResult} />
        );
        const cards = screen.getAllByTestId('play-card');

        fireEvent.click(cards[0]);
        fireEvent.click(cards[2]);
        fireEvent.click(screen.getByTestId('overlay'));
        await screen.findByText('Score: 110');
        expect(cards[0]).toBeDisabled();
        expect(cards[2]).toBeDisabled();
        
        fireEvent.click(cards[1]);
        fireEvent.click(cards[3]);
        fireEvent.click(screen.getByTestId('overlay'));
        await screen.findByText('Score: 120');
        expect(cards[1]).toBeDisabled();
        expect(cards[3]).toBeDisabled();
        expect(submitResult).toHaveBeenCalled();
    });

    it('displays three columns when sections length is less than or equal to 6', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} />);
        expect(container.querySelector('.playing-board--three-columns')).toBeInTheDocument();
    });

    it('displays four columns when sections length is greater than 6', () => {
        const sections = new Array(7).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} />);
        expect(container.querySelector('.playing-board--three-columns')).not.toBeInTheDocument();
    });

    it('displays score feedback when scoreFeedbackDisplay is not HIDDEN', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.LARGE_TOP} />);
        expect(container.querySelector('.matching-pairs__score-feedback')).toBeInTheDocument();
    });

    it('does not display score feedback when scoreFeedbackDisplay is HIDDEN', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.HIDDEN} />);
        expect(container.querySelector('.matching-pairs__score-feedback')).not.toBeInTheDocument();
    });

    it('displays score feedback on the top when scoreFeedbackDisplay is LARGE_TOP', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.LARGE_TOP} />);
        expect(container.querySelector('.matching-pairs__score-feedback--small-bottom-right')).not.toBeInTheDocument();
    });

    it('displays score feedback on the bottom right when scoreFeedbackDisplay is SMALL_BOTTOM_RIGHT', () => {
        const sections = new Array(6).fill({}).map((_, index) => ({ id: index }));
        const { container } = render(<MatchingPairs {...baseProps} sections={sections} scoreFeedbackDisplay={SCORE_FEEDBACK_DISPLAY.SMALL_BOTTOM_RIGHT} />);
        expect(container.querySelector('.matching-pairs__score-feedback--small-bottom-right')).toBeInTheDocument();
    });

});
