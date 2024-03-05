import React from 'react';
import { fireEvent, render, waitFor } from '@testing-library/react';
import MatchingPairs, { SCORE_FEEDBACK_DISPLAY } from './MatchingPairs';

jest.mock("../../util/stores", () => ({
    __esModule: true,
    default: jest.fn(),
    useBoundStore: jest.fn()
}));

describe('MatchingPairs Component', () => {
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
        submitResult: jest.fn(),
        showAnimation: false
    };
    it('renders correctly', () => {
        const { getByText } = render(<MatchingPairs sections={mockSections} setPlayerIndex={jest.fn()} />);
        expect(getByText('Pick a card')).toBeInTheDocument();
    });

    it('flips a card when clicked', async () => {
        const { getAllByTestId } = render(<MatchingPairs sections={mockSections} setPlayerIndex={jest.fn()} />);
        const cards = getAllByTestId('play-card'); // Assuming each card is a button, adjust if necessary

        fireEvent.click(cards[0]);

        await waitFor(() => expect(cards[0]).toHaveClass('turned'));
    });

    it('updates score after a match', async () => {
        const { getAllByTestId, getByTestId } = render(<MatchingPairs sections={mockSections} setPlayerIndex={jest.fn()} />);
        const cards = getAllByTestId('play-card');

        fireEvent.click(cards[0]);
        fireEvent.click(cards[1]);

        await waitFor(() => expect(getByTestId('score')).toBeInTheDocument());
        expect(getByTestId('score')).toHaveTextContent('100');
    });


    it('ends the game when all pairs are matched', async () => {
        const finishedPlaying = jest.fn();
        const submitResult = jest.fn();
        const { getAllByTestId, getByTestId, queryByText } = render(
            <MatchingPairs sections={mockSections} setPlayerIndex={jest.fn()} submitResult={submitResult} finishedPlaying={finishedPlaying} />
        );
        const cards = getAllByTestId('play-card');

        fireEvent.click(cards[0]);
        fireEvent.click(cards[2]);
        fireEvent.click(getByTestId('overlay'));
        fireEvent.click(cards[1]);
        fireEvent.click(cards[3]);
        fireEvent.click(getByTestId('overlay'));

        await waitFor(() => {
            expect(queryByText('Pick a card')).not.toBeInTheDocument();
            expect(submitResult).toHaveBeenCalled();
        });
    });

    it('disables card clicks in-between turns', async () => {
        const { getAllByTestId } = render(<MatchingPairs sections={mockSections} setPlayerIndex={jest.fn()} />);
        const cards = getAllByTestId('play-card');

        await waitFor(() => expect(cards[0]).not.toHaveClass('noevents'));
        await waitFor(() => expect(cards[1]).not.toHaveClass('noevents'));

        fireEvent.click(cards[0]);
        fireEvent.click(cards[1]);

        await waitFor(() => expect(cards[0]).toHaveClass('noevents'));
        await waitFor(() => expect(cards[1]).toHaveClass('noevents'));
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
