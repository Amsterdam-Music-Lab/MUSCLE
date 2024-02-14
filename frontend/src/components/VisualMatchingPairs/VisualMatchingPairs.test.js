import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import VisualMatchingPairs from './VisualMatchingPairs'; // Adjust the import path as necessary

jest.mock("../../util/stores");

// Mock data for sections
const mockSections = [
    { id: 1, content: 'Card 1', url: '/cat-01.jpg', inactive: false, turned: false, noevents: false, seen: false, group: 1 },
    { id: 2, content: 'Card 2', url: '/cat-02.jpg', inactive: false, turned: false, noevents: false, seen: false, group: 2 },
    { id: 3, content: 'Card 1', url: '/cat-01.jpg', inactive: false, turned: false, noevents: false, seen: false, group: 1 },
    { id: 4, content: 'Card 2', url: '/cat-02.jpg', inactive: false, turned: false, noevents: false, seen: false, group: 2 },
];

describe('VisualMatchingPairs', () => {
    it('renders correctly', () => {
        const { getByText } = render(<VisualMatchingPairs sections={mockSections} setPlayerIndex={jest.fn()} />);
        expect(getByText('Pick a card')).toBeInTheDocument();
    });

    it('flips a card when clicked', async () => {
        const { getAllByTestId } = render(<VisualMatchingPairs sections={mockSections} setPlayerIndex={jest.fn()} />);
        const cards = getAllByTestId('play-card'); // Assuming each card is a button, adjust if necessary

        fireEvent.click(cards[0]);

        await waitFor(() => expect(cards[0]).toHaveClass('turned'));
    });

    it('updates score after a match', async () => {
        const { getAllByTestId, getByTestId } = render(<VisualMatchingPairs sections={mockSections} setPlayerIndex={jest.fn()} />);
        const cards = getAllByTestId('play-card');

        fireEvent.click(cards[0]);
        fireEvent.click(cards[1]);

        await waitFor(() => expect(getByTestId('score')).toBeInTheDocument());
        expect(getByTestId('score')).toHaveTextContent('100');
    });

    it('does not update score for a non-matching pair', async () => {
        const { getAllByTestId, getByTestId } = render(<VisualMatchingPairs sections={mockSections} setPlayerIndex={jest.fn()} />);
        const cards = getAllByTestId('play-card');

        fireEvent.click(cards[0]);
        fireEvent.click(cards[1]);

        await waitFor(() => expect(getByTestId('score')).toBeInTheDocument());
        expect(getByTestId('score')).toHaveTextContent('100'); // Assuming 100 is the initial score
    });

    it('ends the game when all pairs are matched', async () => {
        const finishedPlaying = jest.fn();
        const submitResult = jest.fn();
        const { getAllByTestId, getByTestId, queryByText } = render(
            <VisualMatchingPairs sections={mockSections} setPlayerIndex={jest.fn()} submitResult={submitResult} finishedPlaying={finishedPlaying} />
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
        const { getAllByTestId } = render(<VisualMatchingPairs sections={mockSections} setPlayerIndex={jest.fn()} />);
        const cards = getAllByTestId('play-card');

        await waitFor(() => expect(cards[0]).not.toHaveClass('noevents'));
        await waitFor(() => expect(cards[1]).not.toHaveClass('noevents'));

        fireEvent.click(cards[0]);
        fireEvent.click(cards[1]);

        await waitFor(() => expect(cards[0]).toHaveClass('noevents'));
        await waitFor(() => expect(cards[1]).toHaveClass('noevents'));
    });

    it('calculates the correct score for a match', async () => {
        const finishedPlaying = jest.fn();
        const submitResult = jest.fn();
        const { getAllByTestId, getByTestId } = render(<VisualMatchingPairs sections={mockSections} setPlayerIndex={jest.fn()} submitResult={submitResult} finishedPlaying={finishedPlaying} />);
        const cards = getAllByTestId('play-card');

        fireEvent.click(cards[0]);
        fireEvent.click(cards[1]);
        fireEvent.click(getByTestId('overlay'));

        // No match, no score
        await waitFor(() => expect(getByTestId('score')).toHaveTextContent('100'));

        fireEvent.click(cards[0]);
        fireEvent.click(cards[3]);
        fireEvent.click(getByTestId('overlay'));

        // No match, no score
        await waitFor(() => expect(getByTestId('score')).toHaveTextContent('100'));

        fireEvent.click(cards[0]);
        fireEvent.click(cards[2]);
        fireEvent.click(getByTestId('overlay'));

        // Lucky match, +10
        await waitFor(() => expect(getByTestId('score')).toHaveTextContent('110'));

        fireEvent.click(cards[1]);
        fireEvent.click(cards[3]);
        fireEvent.click(getByTestId('overlay'));

        // Known match, +20
        await waitFor(() => expect(getByTestId('score')).toHaveTextContent('130'));
    });
});

